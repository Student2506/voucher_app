import React from "react";
import { useSelector } from "react-redux";

export default React.memo(function Header() {
  const { login } = useSelector(state => state.user.userData)
  return (
    <header className="header">
      <p className="header__account">{ login }</p>
    </header>
  )
}
)
