import React from "react";
import { Link, NavLink, useHistory } from "react-router-dom";

export default React.memo(function NavBar() {

  const history = useHistory();

  return (
    <aside className="navBar">
      <div className="navBar__logo" />
      <h2 className="navBar__title">Сертификаты</h2>
      <nav className="navBar__navigation">
        <NavLink to="/vouchers" activeClassName={"navBar__link_current"} className="navBar__link" >Заказы</NavLink>
        <NavLink to="/refund" activeClassName={"navBar__link_current"} className="navBar__link">Возвраты</NavLink>
        <NavLink to="/time-management" activeClassName={"navBar__link_current"} className="navBar__link">Изменение срока действия сертификата</NavLink>
      </nav>
    </aside>
  )
}
)
