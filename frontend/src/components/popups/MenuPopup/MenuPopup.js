import React from "react";
import { useDispatch } from "react-redux";
import { exitUser } from "../../../utils/store/userSlice";
import { useHistory } from "react-router-dom";

export function MenuPopup({ isOpen, onClose }) {

  const dispatch = useDispatch();
  const history = useHistory();

  function exit() {
    dispatch(exitUser());
    history.push('/sign-in');
  }

  return(
    <article className={`menu ${isOpen ? "menu_open" : ""}`}>
      <div className="menu__head">
        <p className="menu__name">Тут имя</p>
      </div>
      <button className="button button_theme_blue" style={{margin: 0}} onClick={exit}>Выйти</button>
      <button className="button button_icon_close button_place_menu" onClick={() => {onClose()}} />
    </article>
  )
}
