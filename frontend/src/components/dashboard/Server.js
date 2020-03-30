import React from "react";
// import Button from "@material-ui/core/Button";
import Paper from "@material-ui/core/Paper";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles(theme => ({
  paper: {
    background: "#3e3e3e",
    color: "white",
    height: 150,
    width: 335,
    paddingTop: theme.spacing(3),
    paddingLeft: theme.spacing(2),
    marginBottom: theme.spacing(2)
    // paddingBottom: theme.spacing(3)
  },
  button: {
    background: "#3e3e3e",
    color: "white",
    height: 40,
    width: 100
  }
}));

export default function Racks(props) {
  const classes = useStyles();

  return (
    <React.Fragment>
      <Paper className={classes.paper} variant="outlined">
        <Typography variant="subtitle1" color="inherit">
          {props.ip}
        </Typography>
        <Grid container>
          <Grid item xs={3}>
            <Typography variant="caption" color="inherit">
              CPU(%)
            </Typography>
            <Typography variant="h6"> {props.cpu} </Typography>
            {/* <Button className={classes.button}>Expand</Button> */}
          </Grid>
          <Grid item xs={6}>
            <Typography variant="caption" color="inherit">
              Disk Usage(%)
            </Typography>
            <Typography variant="h6"> {props.dsk} </Typography>
          </Grid>
          <Grid item xs={3}>
            <Typography variant="caption" color="inherit">
              Status
            </Typography>
            <Typography variant="h6"> OK </Typography>
          </Grid>
        </Grid>
      </Paper>
    </React.Fragment>
  );
}
