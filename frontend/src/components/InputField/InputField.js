import React from "react";

export default function InputField({onClickButton, onChange, placeholder, fieldClass}) {
  return (
    <fieldset className={`inputField ${fieldClass ? fieldClass : ""}`}>
      <input className="input input_place_vouchers" placeholder={placeholder} onChange={onChange}/>
      <button type={"reset"} className="button button_icon_close button_place_vouchers" onClick={onClickButton} />
    </fieldset>
  )
}
