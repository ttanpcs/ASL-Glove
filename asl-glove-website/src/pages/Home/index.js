import React from "react";
import "./styles.sass";

export default class Home extends React.Component {
  render() {
    return (    
          <div className = "background">
          <div className = "content">
          <div className = "title-box">
            American Sign Language Translation Glove
          </div>
          <div className = "title-box">
            About
          </div>
          <div className = "title-box">
            Plan
          </div>
          <div className = "title-box">
            Members
          </div>
          </div>      

          <div className = "footer">
              <div className = "text">
              Copyright © 2022 Tony Tan
              </div>
              <div className = "text">
              ttanpcs@gmail.com
              </div>
              <div className = "text">
              github.com/goldenxuett
              </div>
          </div>   
      </div>
    )
  }
}