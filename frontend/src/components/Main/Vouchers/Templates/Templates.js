import React, { useState } from "react";
import RadioFake from "../RadioFake/RadioFake";
import circle from "../../../../images/Rolling-1s-200px.svg";
import { useDispatch, useSelector } from "react-redux";
import { pushVoucher } from "../../../../utils/store/customersSlice";

export default function Templates() {

  const dispatch = useDispatch();
  // const templates = useSelector(state => state.customers.templates);

  const {templates, pushStatus, pushError} = useSelector(state => state.customers);

  const [template, setTemplate] = useState('');
  const [email, setEmail] = useState('');
  function handleSubmit(e) {
    e.preventDefault();
    dispatch(pushVoucher({email, template}))
  }

  console.log(pushError);
  console.log(pushStatus);
  return (
    <>
      {
        templates.map((template, index) =>
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
          <input required={true} type="email" className="input input_place_vouchers" placeholder="Введите E-Mail получателя" onChange={(e) => {setEmail(e.target.value)}} />
          <button type={"reset"} className="button button_icon_close button_place_vouchers" />
        </fieldset>
        {
          pushStatus === 'resolved' || pushStatus === 'rejected'
            ? <span
              className={`templates__progress ${!pushError ? "templates__progress_success" : "templates__progress_failure"}`}
            >
              {!pushError ? "Все прошло успешно. Ваучеры высланы на почту" : "Что-то пошло не так, попробуйте еще раз."}
          </span>
            : <></>
        }
        <button type="submit" className={`button button_theme_blue button_place_vouchers-main`}>{pushStatus === 'loading' ? <img src={circle} className="button_preload"/> : "Подтвердить"}</button>
      </form>
    </>
  )
}
