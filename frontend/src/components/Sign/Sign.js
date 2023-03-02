import logo from "../../images/logo.png"
import circle from "../../images/Rolling-1s-200px.svg"
import { useState } from "react";
import { useDispatch } from "react-redux";
import { fetchUser } from "../../store/userSlice";
import { useHistory } from "react-router-dom";

export default function Sign({ preload }) {

  const [login, setLogin] = useState('');
  const [pass, setPass] = useState('');

  const dispatch = useDispatch();

  function handleSubmit(e) {
    e.preventDefault();
    // dispatch(fetchUser({login, pass}));
  }

  return (
    <section className="sign">
      <div className="sign__container">
        <img src={logo} className="sign__logo"/>
        <h2 className="sign__title">Сертификаты</h2>
        <form className="sign__form" onSubmit={handleSubmit}>
          <label htmlFor="user-name" className="sign__label">Имя пользователя</label>
          <input
            type="text"
            name="user-name"
            id="user-name"
            className="input input_place_sign"
            value={login}
            onChange={(e) => {setLogin(e.target.value)}}
          />
          <label htmlFor="user-password" className="sign__label">Пароль</label>
          <input
            type="password"
            name="user-password"
            id="user-password"
            className="input input_place_sign"
            value={pass}
            onChange={(e) => {setPass(e.target.value)}}
          />
          <button type="submit" className="button button_theme_blue">
            {/*{preload ? <img src={circle} className="button_preload"/> : "Войти"}*/}
            <a href={"http://10.0.10.234/api/v1/oauth2/login"}>Войти</a>
          </button>
        </form>
      </div>
      <div className="sign__bg" />
    </section>
  )
}
