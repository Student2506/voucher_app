'use strict'

const partnerChoiceTemplate = document.querySelector('#partner-choice__template');
const partnerChoiceSection = document.querySelector('.partner-choice');
const partnersArr = [
    {
      name: 'KAРO Фильм Менеджмент',
      href: '',
      src: 'images/logo-sqr.png',
    },
  {
    name: 'Тинькофф',
    href: '',
    src: 'https://pictures.s3.yandex.net/frontend-developer/cards-compressed/arkhyz.jpg',
  },
  {
    name: 'Тинькофф',
    href: '',
    src: 'https://pictures.s3.yandex.net/frontend-developer/cards-compressed/arkhyz.jpg',
  }
];

function makeCard (configObject) {
  const card = partnerChoiceTemplate.content.cloneNode(true);
  const cardImage = card.querySelector('.partner-choice__image');
  const cardLink = card.querySelector('.partner-choice__link');
  const cardButton = card.querySelector('.button_place_chooseAgent');
  card.querySelector('.partner-choice__caption').textContent = configObject.name;
  cardLink.setAttribute('href', configObject.href);
  cardImage.setAttribute('src', configObject.src);
  return card;
}

function preloadImage (configArr) {
  configArr.forEach(function (configObject) {
    const card = makeCard(configObject);
    partnerChoiceSection.prepend(card);
  });
};

preloadImage(partnersArr);