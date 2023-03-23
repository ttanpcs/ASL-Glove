import React from "react";
import "../styles.sass";

import Button from "../Button/button"

export default class Home extends React.Component {
  
  
 
  goto(s) {
    window.location.href = s
  }


  render() {
    
    return (    
          <div className = "background">
          <div className = "content">
          <div className = "title-box">
            <div className = "title">SignAlong</div>
            <div className = "menu"><Button className = "dropdown-button"></Button></div>
          </div>
          
          </div>      

      </div>
    )
  }
}