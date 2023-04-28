import React from 'react';
import logo from '../../images/logo.png';
import { BASE_URL } from "../../constants";
import styles from '../../styles/sign-in.scss';

const SignIn = () => {
  return (
    <section className="sign">
      <div className="sign__container">
        <img src={logo} className="sign__logo"/>
        <h2 className="sign__title">Сертификаты</h2>
        <button type="submit" className="button button_theme_blue">
          <a className="sign__link" href={`${BASE_URL}/api/v1/oauth2/login`}>Войти</a>
        </button>
      </div>
      <div className="sign__bg" />
    </section>
  );
};

export default SignIn;
