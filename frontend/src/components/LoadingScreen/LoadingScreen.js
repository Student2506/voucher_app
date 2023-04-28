import logo from '../../images/logo.png'
import styles from '../../styles/loadingScreen.scss';

export default function LoadingScreen() {
  return (
    <div className="loadingScreen">
      <img className="loadingScreen__logo" src={logo} />
      <div className="loadingScreen__bar" />
    </div>
  )
}
