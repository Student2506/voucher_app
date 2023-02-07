export default function RadioFake(props) {
  return (
    <fieldset className="order">
      <input {...props} type={"radio"} className="order__input" name={`customer-${props.name}`} id={`customer-order${props.id}`} />
      <label htmlFor={`customer-order${props.id}`} className="order__fake">{props.description}</label>
    </fieldset>
  )
}
