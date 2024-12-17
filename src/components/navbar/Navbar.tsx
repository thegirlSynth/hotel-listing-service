import styles from './Navbar.module.css';

function Navbar() {
  return (
    <div className={styles.navbar}>
    <a href="/" className={styles.navLink}>Home</a>
    <a href="/about" className={styles.navLink}>About</a>
    <a href="/contact" className={styles.navLink}>Contact</a>
  </div>
  )
}

export default Navbar
