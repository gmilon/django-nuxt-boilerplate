const baseUrl = 'http://localhost:3000/'
context('SignUp health', function () {
  it('Should be able to access signUp from login page', function () {
    cy.visit('/login')
    cy.contains('Sign Up')
    cy.get('p > a').click()

    cy.contains('Password')
    cy.contains('Password Confirmation')
    cy.contains('Email')
  })
})
context('SignUp Form', function () {
  beforeEach(() => {
    cy.server()
    cy.visit('/login')
    cy.get('p > a').click()
  })
  it('Should show an error on wrong email', function () {
    cy.get('#email').type('tagada@')
    cy.contains('E-mail must be valid')
  })
  it('Should show an error on short password', function () {
    cy.get('#password').type('ta')
    cy.contains('Password is too short')
  })
  it('Should show an error on weak password', function () {
    cy.get('#password').type('tagadatagada')
    cy.contains('Password is too weak')
  })
  it('Should show an error when password are not matching', function () {
    cy.get('#password').type('Extrem17220')
    cy.get('#password-confirmation').type('Someth1gnElse')
    cy.contains('Passwords are not matching')
  })
  it('Sign Up button should be disabled on Empty form', function () {
    cy.get('#submit').should('have.prop', 'disabled', true)
  })
  it('Sign Up button should be disabled on invalid form', function () {
    cy.get('#password').type('notValidpwd')
    cy.get('#submit').should('have.prop', 'disabled', true)
  })
  it('Should be able to submit if the form is valid', function() {
    cy.get('#email').type('excellent@gmail.com')
    cy.get('#password').type('tagada2strong')
    cy.get('#password-confirmation').type('tagada2strong')
    cy.get('#submit').should('have.prop', 'disabled', false)
  })
  it('Should throw an error if the username already exists', function() {
    cy.route({
      method: 'POST',
      url: 'api/auth/users/',
      response: 'fx:auth/users_already_exists.json',
      status: 400
    })
    cy.get('#email').type('excellent@gmail.com')
    cy.get('#password').type('tagada2strong')
    cy.get('#password-confirmation').type('tagada2strong')
    cy.get('#submit').click()
    cy.contains('A user with that username already exists.')
  })
  it('Should redirect to home page if the form is valid', function() {
    cy.route({
      method: 'POST',
      url: 'api/auth/users/',
      response: 'fx:auth/users_success.json',
      status: 200
    })
    cy.route({
      method: 'POST',
      url: 'api/auth/token/login',
      response: 'fx:auth/token_success.json',
      status: 200
    })
    cy.get('#email').type('excellent@gmail.com')
    cy.get('#password').type('tagada2strong')
    cy.get('#password-confirmation').type('tagada2strong')
    cy.get('#submit').click()
    cy.url().should('eq', baseUrl)
  })
})
