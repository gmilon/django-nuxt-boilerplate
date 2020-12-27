const baseUrl = 'http://localhost:3000/'
context('Continue With Goole', function () {
  it('Should Show A Waiting Message', function () {
    cy.visit('/oauth')
    cy.contains('Verifying Your account')
    cy.contains('Redirecting...')
  })
  it('Should show an error message if auth failed', function () {
    cy.visit('/oauth')
    cy.intercept('POST', '/api/auth/google/', {
      statusCode: 400,
    })
    cy.contains('Cannot login using Google, please try again later')
  })
  it('Should redirect to home if successs', function () {
    cy.intercept('POST', '/api/auth/google/', {
      fixture: 'auth/token_success',
    })
    cy.visit('/oauth')
    cy.contains('Welcome !')
    cy.url().should('eq', baseUrl)
  })
})
