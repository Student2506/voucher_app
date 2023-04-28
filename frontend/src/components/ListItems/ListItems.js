import React, { useState } from 'react';
import style from '../../styles/listItem.scss'

const ListItems = ({title, extraClasses, type, uniqueKey, onClickItem, listName, value, checked}) => {
  return (
    <div className={`list-item ${extraClasses ? extraClasses : ""}`}>
      <input
        className={"list-item__input"}
        name={`list-item-${listName}`}
        type={type ? type : "radio"}
        checked={checked}
        id={`list-${uniqueKey}-${listName}`}
        value={value ? value : ""}
        onChange={onClickItem}/>
      <label className={"list-item__label"} htmlFor={`list-${uniqueKey}-${listName}`}>{title}</label>
    </div>
  );
};

export default ListItems;
