import React from "react";
import Paper from "@material-ui/core/Paper";
import Grid from "@material-ui/core/Grid";
import ExpansionPanel from "@material-ui/core/ExpansionPanel";
import ExpansionPanelDetails from "@material-ui/core/ExpansionPanelDetails";
import ExpansionPanelSummary from "@material-ui/core/ExpansionPanelSummary";
import Typography from "@material-ui/core/Typography";
import ExpandMoreIcon from "@material-ui/icons/ExpandMore";
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
  position: {
    paddingRight: theme.spacing(3)
  },
}));

export default function Racks(props) {
  const classes = useStyles();

  return (
    <React.Fragment>
      <ExpansionPanel>
        <ExpansionPanelSummary
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel1a-content"
          id="panel1a-header"
        >
          <Typography variant="subtitle1" className={classes.position}>{props.position}.</Typography>
          <Typography variant="subtitle1">{props.ip}</Typography>
        </ExpansionPanelSummary>
        <ExpansionPanelDetails>
          <Paper className={classes.paper} variant="outlined">
            <Typography variant="subtitle1" color="inherit">
              {props.os}
            </Typography>
            <Grid container>
              <Grid item xs={3}>
                <Typography variant="caption" color="inherit">
                  CPU(%)
                </Typography>
                <Typography variant="h6"> {props.cpu} </Typography>
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
        </ExpansionPanelDetails>
      </ExpansionPanel>
    </React.Fragment>
  );
}
