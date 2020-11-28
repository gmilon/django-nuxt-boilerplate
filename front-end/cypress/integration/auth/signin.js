const baseUrl = 'http://localhost:3000/'

context('Sign In Form', function() {
  beforeEach(() => {
    cy.server()
    cy.visit('/login')
  })
  it('Should show an error on wrong email', function() {
    cy.get('#email').type('teeeee.dsds')
    cy.contains('E-mail must be valid')
  })
  it('Should hide the password', function() {
    cy.get('#password').type('tagada')
    cy.should('not.contain', 'tagada')
  })
  it('Should show the password', function() {
    cy.get('#password').type('tagada')
    cy.get('.v-icon').click()
    cy.get('#password').should('have.attr', 'type', 'text')
  })
  it('Should not be able to submit on invalid form', function() {
    cy.get('#email').type('something wrong')
    cy.get('#password').type('toS')
    cy.get('#submit').should('have.prop', 'disabled', true)
  })
})
