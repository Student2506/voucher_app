import React, { useRef } from 'react';
import style from '../../styles/searchInput.scss';

const SearchInput = ({ type, extraClassesInput, extraClassesContainer, onChangeInput, onClickButton, placeholder, name, required }) => {

  const inputRef = useRef();

  return (
    <fieldset className={`search-input ${extraClassesContainer ? extraClassesContainer : ""}`}>
      <div>
        <input required={required} ref={inputRef} placeholder={placeholder ? placeholder : ""} className={`${extraClassesInput ? extraClassesInput : ""}`} onChange={onChangeInput} type={type} name={name ? name : ""}/>
        <button className={"search-input__reset"} onClick={() => {
          onClickButton();
          inputRef.current.value = '';
        }} type={"button"}></button>
      </div>
    </fieldset>
  );
};

export default SearchInput;
