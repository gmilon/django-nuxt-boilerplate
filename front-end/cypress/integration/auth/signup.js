let baseUrl = ' '
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
    cy.visit('/login')
    cy.get('p > a').click()
  })
  it('Should show an error on wrong email', function () {
    goToSignUp()
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
    cy.get('#password').type('Extrem17')
    cy.get('#password-confirmation').type('Someth1gnElse')
    cy.contains('Password are not matching')
  })
  it('Sign Up button should be disabled on invalid form', function () {
    cy.get('#submit')
  })
})
