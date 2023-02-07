import logo from '../../images/logo.png'

export default function LoadingScreen() {
  return (
    <div className="loadingScreen">
      <img className="loadingScreen__logo" src={logo} />
      <div className="loadingScreen__bar" />
    </div>
  )
}
