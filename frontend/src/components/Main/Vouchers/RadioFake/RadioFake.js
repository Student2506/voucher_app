export default function RadioFake(props) {
  return (
    <fieldset className="radioFake">
      <input {...props} type={"radio"} className="radioFake__input" name={`customer-${props.name}`} id={`customer-order${props.id}`} defaultChecked={props.checked} />
      <label htmlFor={`customer-order${props.id}`} className="radioFake__fake">{props.description}</label>
    </fieldset>
  )
}
