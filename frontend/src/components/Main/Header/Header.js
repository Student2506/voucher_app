import React, { useState } from "react";
import { useSelector } from "react-redux";
import cross from '../../../images/cross.svg';
import { MenuPopup } from "../../popups/MenuPopup/MenuPopup";

export default React.memo(function Header() {
  const { login } = useSelector(state => state.user.userData)
  const [popupOpen, setPopupOpen] = useState(false);

  function closePopup() {
    setPopupOpen(false);
  }

  return (
    <header className="header">
      {/*<p className="header__account">{ login }</p>*/}
      <p className="header__account" onClick={() => {setPopupOpen(true)}}>Нажми на меня</p>
      <MenuPopup isOpen={popupOpen} onClose={closePopup}/>
    </header>
  )
}
)
