import React from 'react';
import { NavLink } from "react-router-dom";
import style from "../../styles/navbar.scss";
import logo from "../../images/logo.png"

const Navbar = () => {
  return (
    <section className={"navbar"}>
      <div className={"navbar__logo"}/>
      <h1 className={"navbar__title"}>Сертификаты</h1>
      <nav className={"navbar__navigation"}>
        <NavLink to={"/vouchers"} className={"navbar__link"} activeClassName={"navbar__link_active"}>Заказы</NavLink>
        <NavLink to={"/refund"} className={"navbar__link"} activeClassName={"navbar__link_active"}>Возвраты</NavLink>
        <NavLink to={"/change"} className={"navbar__link"} activeClassName={"navbar__link_active"}>Изменения срока действия сертификата</NavLink>
        <NavLink to={"/template"} className={"navbar__link"} activeClassName={"navbar__link_active"}>Шаблоны</NavLink>
      </nav>
    </section>
  );
};

export default Navbar;
