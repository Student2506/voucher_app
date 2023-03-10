import logo from "../../images/logo.png"
export default function Sign() {

  function handleSubmit(e) {
    e.preventDefault();
  }

  return (
    <section className="sign">
      <div className="sign__container">
        <img src={logo} className="sign__logo"/>
        <h2 className="sign__title">Сертификаты</h2>
        {/*<form className="sign__form" onSubmit={handleSubmit}>*/}
        {/*  <label htmlFor="user-name" className="sign__label">Имя пользователя</label>*/}
        {/*  <input*/}
        {/*    type="text"*/}
        {/*    name="user-name"*/}
        {/*    id="user-name"*/}
        {/*    className="input input_place_sign"*/}
        {/*  />*/}
        {/*  <label htmlFor="user-password" className="sign__label">Пароль</label>*/}
        {/*  <input*/}
        {/*    type="password"*/}
        {/*    name="user-password"*/}
        {/*    id="user-password"*/}
        {/*    className="input input_place_sign"*/}
        {/*  />*/}
        {/*</form>*/}
        <button type="submit" className="button button_theme_blue">
          <a className="sign__link" href={"http://10.0.10.234/api/v1/oauth2/login"}>Войти</a>
        </button>
      </div>
      <div className="sign__bg" />
    </section>
  )
}
