import React from "react";
import { useDispatch } from "react-redux";
import { clearSession } from "../../../utils/store/userSlice";
import { useHistory } from "react-router-dom";

export function MenuPopup({ isOpen, onClose, login }) {

  const dispatch = useDispatch();
  const history = useHistory();

  function exit() {
    dispatch(clearSession);
    history.push('/sign-in');
  }

  return(
    <article className={`menu ${isOpen ? "menu_open" : ""}`}>
      <div className="menu__head">
        <p className="menu__name">{ login }</p>
      </div>
      <button className="button button_theme_blue" style={{margin: 0}} onClick={exit}>
        <a href={'https://adfs.karo-film.ru/adfs/oauth2/logout'}>Выйти</a>
      </button>
      <button className="button button_icon_close button_place_menu" onClick={() => {onClose()}} />
    </article>
  )
}
