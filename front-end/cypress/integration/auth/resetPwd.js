const baseUrl = 'http://localhost:3000/'

context('Forgot password Link', function () {
  it('Sould show an error on wrong token', function () {
    cy.intercept('POST', '/api/auth/password/reset/confirm/', {
      statusCode: 400,
      fixture: 'auth/reset_password_confirm_error',
    })
    cy.visit('/reset-password/wrong-token')
    cy.get('#password').type('ImStrong1212')
    cy.get('#password-confirmation').type('ImStrong1212')
    cy.get('#submit').click()
    cy.contains('Sorry, cannot verify your identity')
  })

  it('Sould show an error on wrong uid', function () {
    cy.intercept('POST', '/api/auth/password/reset/confirm/', {
      statusCode: 400,
      fixture: 'auth/reset_password_confirm_error_uid',
    })
    cy.visit('/reset-password/wrong-token')
    cy.get('#password').type('ImStrong1212')
    cy.get('#password-confirmation').type('ImStrong1212')
    cy.get('#submit').click()
    cy.contains('Sorry, cannot verify your identity')
  })

  it('Should show an error on weak password', function () {
    cy.visit('/reset-password/super-token')
    cy.get('#password').type('tagadatagada')
    cy.contains('Password is too weak')
  })

  it('Should show an error on short password', function () {
    cy.visit('/reset-password/super-token')
    cy.get('#password').type('short')
    cy.contains('Password is too short')
  })

  it("Should show an error if password don't match", function () {
    cy.visit('/reset-password/super-token')
    cy.get('#password').type('ImStrong1212')
    cy.get('#password-confirmation').type('ImStrong1213')
    cy.contains('Passwords are not matching')
  })

  it('Should not be able to sumbit form if form is not valid', function () {
    cy.visit('/reset-password/super-token')
    cy.get('#submit').should('have.prop', 'disabled', true)
    cy.get('#password').type('weak')
    cy.get('#submit').should('have.prop', 'disabled', true)
  })

  it('Should be able to submit form on valid form', function () {
    cy.intercept('POST', '/api/auth/password/reset/confirm/', {
      fixture: 'auth/reset_password_confirm',
    })
    cy.visit('/reset-password/super-token')
    cy.get('#password').type('ImStrong1212')
    cy.get('#password-confirmation').type('ImStrong1212')
    cy.get('#submit').should('have.prop', 'disabled', false).click()
    cy.url().should('eq', baseUrl + 'login')
  })
})
