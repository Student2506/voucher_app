import React, { useState } from "react";
import RadioFake from "../RadioFake/RadioFake";
import circle from "../../../../images/Rolling-1s-200px.svg";

export default function Templates({ orderTemplates, onSubmit, orderId, preload, success }) {

  const [email, setEmail] = useState('');
  const [template, setTemplate] = useState('');

  function handleSubmit(e) {
    e.preventDefault();
    onSubmit(orderId, template, email);
  }

  return (
    <>
      {
        orderTemplates.map((template, index) =>
          <RadioFake
            value={Object.keys(template).map((key) => key)}
            id={index + 20000}
            key={index}
            description={Object.values(template).map((val) => val)}
            name={"template"}
            onChange={(e) => {setTemplate(e.target.value)}}
          />
        )
      }
      <form className="templates__form" onSubmit={handleSubmit}>
        <fieldset className="templates__filed">
          <input required={true} onChange={(e) => {setEmail(e.target.value)}} type="email" className="input input_place_vouchers" placeholder="Введите E-Mail получателя"/>
          <button type={"reset"} className="button button_icon_close button_place_vouchers" onClick={() => {setEmail('')} }/>
        </fieldset>
        {
          success.templateSection === true || success.templateSection === false
            ? <span
              className={`templates__progress ${success.templateSection ? "templates__progress_success" : "templates__progress_failure"}`}
            >
              {success.templateSection ? "Все прошло успешно. Ваучеры высланы на почту" : "Что-то пошло не так, попробуйте еще раз."}
          </span>
            : <></>
        }
        <button type="submit" className={`button button_theme_blue button_place_vouchers-main`}>{preload ? <img src={circle} className="button_preload"/> : "Подтвердить"}</button>
      </form>
    </>
  )
}
