const baseUrl = 'http://localhost:3000/'

context('Forgot password Form', function () {
  beforeEach(() => {
    cy.visit('/login')
    cy.get('#forgot-pwd').click()
  })
  it('Should show an error on wrong email', function () {
    cy.get('#email').type('teeeee.dsds')
    cy.contains('E-mail must be valid')
  })
  it('Should show the right fields', function () {
    cy.get('#password').should('not.exist')
    cy.get('#password-confirmation').should('not.exist')
  })
  it('Should not be able to submit on invalid Form', function () {
    cy.get('#email').type('Something Wrong')
    cy.get('#submit').should('have.prop', 'disabled', true)
  })
  it("Should show an error if the email doesn't exists", function () {
    cy.intercept("POST", "/api/auth/users/reset_password/", {
      statusCode: 400,
      fixture: "auth/password_reset_error",
    })
    cy.get('#email').type('test@email.com')
    cy.get('#submit').should('have.prop', 'disabled', false).click()
    cy.contains('A user with that username already exists.')
  })
  it('Should be able to submit the form on valid info and show a success Message', function () {
    cy.intercept("POST", "/api/auth/users/reset_password/", {
      fixture: "auth/password_reset_success",
    })
    cy.get('#email').type('test@email.com')
    cy.get('#submit').should('have.prop', 'disabled', false).click()
    cy.contains('A reset email has been sent to test@email.com')
  })
})
