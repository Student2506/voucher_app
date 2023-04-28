import React from 'react';
import header from '../../styles/header.scss'
import Account from "../Account/Account";

const Header = () => {
  return (
    <header className={"header"}>
      <Account extraClass={"header__account"}/>
    </header>
  );
};

export default Header;
