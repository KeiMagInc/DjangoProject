# Created by kerll at 7/29/2025
Feature: Registro de un nuevo producto

  Scenario: Un usuario agrega un nuevo producto al catálogo
    Given que soy un usuario autenticado
    When voy a la página de "agregar producto"
    And relleno el nombre con "Laptop Pro" y el precio con "1500.00"
    And presiono el botón "Guardar"
    Then debería ser redirigido a la página de detalles del producto "Laptop Pro"
    And la base de datos debe contener un producto con el nombre "Laptop Pro"