describe('Dashboard Metrics', () => {
  it('should display system metrics', () => {
    cy.visit('/dashboard');
    cy.get('h1').contains('System Metrics').should('be.visible');
  });

  it('should handle image uploads', () => {
    cy.visit('/dashboard');
    cy.get('input[type="file"]').attachFile('test-image.png');
    cy.get('button').contains('Upload').click();
    cy.get('.uploaded-image').should('be.visible');
  });
});