import React from "react";

export default function InputField({onClickButton, onChange, placeholder, fieldClass, inputType, minMax}) {
  return (
    <fieldset className={`inputField ${fieldClass ? fieldClass : ""}`}>
      <input type={inputType ? inputType : "text"} minLength={minMax.min} maxLength={minMax.max} className="input input_place_vouchers" placeholder={placeholder} onChange={onChange}/>
      <button type={"reset"} className="button button_icon_close button_place_vouchers" onClick={onClickButton} />
    </fieldset>
  )
}
