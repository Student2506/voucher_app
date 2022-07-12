'use strict'

const linkTemplate = document.createElement('a');
const ordersBox = document.querySelector('.orders__box');
const configOrdersObj = [
  {
    href: 'refactorOrder.html',
    order: 'NiceNameOrder'
  },
  {
    href: 'refactorOrder.html',
    order: '112211112211'
  },
  {
    href: 'refactorOrder.html',
    order: 1231212312
  }
];

function createOrder (orderElement, hrefElement) {
  const linkTemplateClone = linkTemplate.cloneNode('true');
  linkTemplateClone.setAttribute('href', hrefElement);
  linkTemplateClone.textContent = orderElement;
  linkTemplateClone.classList.add('orders__link');
  return linkTemplateClone;
}

function preloadOrders (configObj) {
  configObj.forEach((orderElement) => {
    const order = createOrder(orderElement.order, orderElement.href);
    ordersBox.append(order);
  })
}

preloadOrders (configOrdersObj);