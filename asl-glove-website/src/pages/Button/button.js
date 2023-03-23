import React from "react";
global.index = 10
function goto(s) {
    window.location.href = s
}
const Button = () => {
    const [open, setOpen] = React.useState(false);
    const handleOpen = function() {
      setOpen(!open);
    }
    return (
      <div>
        <button className = "menu-button" onClick={handleOpen}>Menu</button>
        {open ? (
          <ul className="list">
            <li>
              <button className="list-item" onClick={()=>goto("./")}>Home</button>
            </li>
            <li>
              <button className="list-item" onClick={()=>goto("./registration")}>Register a glove</button>
            </li>
            <li>
              <button className="list-item" onClick={()=>goto("./calibration")}>Calibrate your glove</button>
            </li>
            <li>
              <button className="list-item" onClick={()=>goto("./game")}>Game</button>
            </li>
            <li>
              <button className="list-item" onClick={()=>goto("./signyourname")}>Sign Your Name</button>
            </li>
          </ul>
        ) : null}
      </div>
    )
  }
  export default Button;