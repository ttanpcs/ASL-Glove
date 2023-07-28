import React from "react";
import "./signstyles.sass";
import Button from "../Button/button"
import { left_glove_state, right_glove_state } from "../../App";
import {useRecoilValue, useSetRecoilState} from 'recoil'
import useSound from 'use-sound'
import clapSFX from '../../assets/clap.mp3'


const GameBox = (rightid) => {
  const [active, setActive] = React.useState(false);
  const [startTime, setStartTime] = React.useState(0);
  const [runTime, setRunTime] = React.useState(0);
  const alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z",];
  const [timeOut, setTimeOut] = React.useState(false)
  const [tempName, setTempName] = React.useState("")
  const [name, setName] = React.useState("")
  const [runningName, setRunningName] = React.useState("")
  const [play] = useSound(clapSFX)

  const Start = async () => {
    console.log(rightid)
    const response = await fetch('http://localhost:5000/reset', {
          method: 'POST',
          headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
          },
        });
    await response.text()
    const response2 = await fetch('http://localhost:5000/start', {
     method: 'POST',
     headers: {
       Accept: 'application/json',
       'Content-Type': 'application/json',
     },
     body: JSON.stringify({glove_id: rightid.rightid.id, ocid: rightid.rightid.open_id, ccid: rightid.rightid.close_id})
   });
    await response2.text()
  }
  
  const Querying = async (num, letter) => {
    var done = false
    if (!done) {
      const response = await fetch('http://localhost:5000/query', {
          method: 'POST',
          headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({label: letter, primary: rightid.rightid.id})
        });
      done = (await response.json()).found
    }
    if (!done && num < 3) {
      await Querying(num + 1, letter)
    }
  }
  
  const Stop = async () => {
    console.log(rightid.rightid.id)
    const response = await fetch('http://localhost:5000/stop', {
          method: 'POST',
          headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({glove_id: rightid.rightid.id})
        });
    await response.text()
  }
  
  const runTimer = async () => {
    const d = new Date()
    if (active) {
      console.log(active)
      const newTime = d.getTime()-startTime
      setRunTime(newTime)
      console.log(startTime)
      await new Promise(resolve => setTimeout(resolve, 990));
      runTimer()
    }
  }

  const runGame = async () => {
    if (runningName != name) {
      let runningLength = runningName.length
      let letter = name[runningLength]
      await Start(rightid)
      await Querying(0, letter)
      await Stop(rightid.glove_id)
      setActive(true)
      setRunningName(runningName + letter)
      console.log(runningName)
    } else {
      await new Promise(resolve => setTimeout(resolve, 990));
      play()
      setActive(false)
    }
  }

  React.useEffect(() => {
    const startGame = async () => {
      if (active) {
        runGame()
      }
    }
    startGame()
  }, [active, runningName])

  const handleSubmit = async (event) => {
    setRunningName("")
    event.preventDefault()
    alert("You submitted your name")
    setActive(true)
  }

  return (
    <div className="namegame">
    <div className="chart"/>
    {!active ? (
      <div>
        <form className="name-form" onSubmit={handleSubmit}>
        <label>Enter your name:&nbsp; &nbsp; &nbsp;
          <input type="text" className="text-input" value = {name} onChange={(e) => setName(e.target.value)}/>
        </label>
        <input type = "submit" className = "name-button" value = "Submit"></input>
        </form>
      </div>
    ) : <div>
      <div className="promptname"> Sign your name, letter by letter</div>
      <div className="showname">{runningName}</div>
      </div>}
    </div>
  )
 
}

export default function SignName() {
  
  const leftid = useRecoilValue(left_glove_state)
  const setLeftId = useSetRecoilState(left_glove_state)
  const rightid = useRecoilValue(right_glove_state)
  const setRightId = useSetRecoilState(right_glove_state)

    
    return (    
          <div className = "background">
          <div className = "content">
          <div className = "title-box">
            <div className = "title">SignAlong</div>
            <div className = "menu"><Button className = "dropdown-button"></Button></div>
          </div>
          <div className="body">
            <GameBox rightid = {rightid}></GameBox>
          </div>
          </div>      

          
      </div>
    )
}