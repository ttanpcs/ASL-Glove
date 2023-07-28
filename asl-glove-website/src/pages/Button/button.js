import React from "react";

 
function goto(s) {
  window.location.replace(s)
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
              <button className="list-item" onClick={()=>goto('/')}>Home</button>
            </li>
            <li>
              <button className="list-item" onClick={()=>goto('/registration')}>Register Gloves</button>
            </li>
            <li>
              <button className="list-item" onClick={()=>goto('/calibration')}>Calibrate Gloves</button>
            </li>
            <li>
              <button className="list-item" onClick={()=>goto('/game')}>Flashcard Game</button>
            </li>
            <li>
              <button className="list-item" onClick={()=>goto('/signyourname')}>Sign Your Name</button>
            </li>
          </ul>
        ) : null}
      </div>
    )
  }
  export default Button;