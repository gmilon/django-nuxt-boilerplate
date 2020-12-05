const baseUrl = 'http://localhost:3000/'

context('Forgot Pwd Form', function () {
  beforeEach(() => {
    cy.server()
    cy.visit('/login')
    cy.get("#forgot-pwd").click()
  })
  it('Should show an error on wrong email', function () {
    cy.get('#email').type('teeeee.dsds')
    cy.contains('E-mail must be valid')
  })
  it("Should show the right fields", function () {
    cy.get('#password').should('not.exist');
    cy.get('#password-confirmation').should('not.exist');
  })
  it("Should not be able to submit on invalid Form", function () {
    cy.get("#email").type('Something Wrong')
    cy.get('#submit').should('have.prop', 'disabled', true)
  })
  it('Should show an error if the email dosen\'t exists', function () {
    
  })
  it('Should be able to submit the form on valid info and show a success Message', function () {

  })
})
