import logo from "../../images/logo.png"

export default function Sign({ onSubmit }) {

  function handleSubmit(e) {
    e.preventDefault();
    onSubmit();
  }

  return (
    <section className="sign">
      <div className="sign__container">
        <img src={logo} className="sign__logo"/>
        <h2 className="sign__title">Ваучеры</h2>
        <form className="sign__form" onSubmit={handleSubmit}>
          <label htmlFor="user-name" className="sign__label">Имя пользователя</label>
          <input
            type="text"
            name="user-name"
            id="user-name"
            className="input input_place_sign"
          />
          <label htmlFor="user-password" className="sign__label">Пароль</label>
          <input
            type="password"
            name="user-password"
            id="user-password"
            className="input input_place_sign"
          />
          <button type="submit" className="button button_theme_blue">Войти</button>
        </form>
      </div>
      <div className="sign__bg" />
    </section>
  )
}
