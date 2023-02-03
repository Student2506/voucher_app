'use strict'

const logonForm = document.querySelector('.logon__form');
const inputLogin = logonForm.querySelector('.logon__input_type_email');
const inputPass = logonForm.querySelector('.logon__input_type_password')
const link = logonForm.querySelector('.sosSOS');
const submitButton = logonForm.querySelector('.button_type_submit');

function disableValidate () {
  logonForm.addEventListener('submit', (evt) => {
    evt.preventDefault();
  })
}

function checkLogin() {
  if (inputLogin.value === 'smersh' && inputPass.value === 'smersh') {
    link.setAttribute('href', 'chooseAgent.html');
  }
}

submitButton.addEventListener('click', checkLogin);