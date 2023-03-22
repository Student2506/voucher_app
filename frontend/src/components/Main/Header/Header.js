import React, { useState } from "react";
import { useSelector } from "react-redux";
import { MenuPopup } from "../../popups/MenuPopup/MenuPopup";

export default React.memo(function Header() {
  const { login } = useSelector(state => state.user.userData)
  const [popupOpen, setPopupOpen] = useState(false);

  function closePopup() {
    setPopupOpen(false);
  }

  return (
    <header className="header">
      <p className="header__account" onClick={() => {setPopupOpen(true)}}>{ login }</p>
      <MenuPopup isOpen={popupOpen} onClose={closePopup} login={login}/>
    </header>
  )
}
)
