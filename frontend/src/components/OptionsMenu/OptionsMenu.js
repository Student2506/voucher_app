import React from 'react';
import './OptionsMenu.scss';

const OptionsMenu = (props) => {
  return (
    <menu className={"menu"}>
      {props.children}
    </menu>
  );
};

export default OptionsMenu;
