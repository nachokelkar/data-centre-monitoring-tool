import React from "react";
import Button from "@material-ui/core/Button";
import Paper from "@material-ui/core/Paper";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles(theme => ({
  paper: {
    background: "#3e3e3e",
    color: "white",
    paddingTop: theme.spacing(3),
    paddingLeft: theme.spacing(2),
    marginBottom: theme.spacing(2)
    // paddingBottom: theme.spacing(3)
  },
  button: {
    background: "#3e3e3e",
    color: "white",
    marginBottom: theme.spacing(2)
  }
}));

export default function Racks(props) {
  const classes = useStyles();

  return (
    <React.Fragment>
      <Paper className={classes.paper} variant="outlined">
        {/*To Do: Typography  */}
        CPU(%) {props.cpu}
        <br />
        127.0.0.1
        <br />
        <Button className={classes.button}>Expand</Button>
      </Paper>
    </React.Fragment>
  );
}
