import React from "react";
// import Button from "@material-ui/core/Button";
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
  button: {
    background: "#3e3e3e",
    color: "white",
    height: 40,
    width: 100
  },
  heading: {
    fontSize: theme.typography.pxToRem(15),
    fontWeight: theme.typography.fontWeightRegular,
  },
}));

export default function Racks(props) {
  const classes = useStyles();
  const [expanded, setExpanded] = React.useState(false);

  const handleChange = panel => (event, isExpanded) => {
    setExpanded(isExpanded ? panel : false);
  };

  return (
    <React.Fragment>
      {/* <Paper className={classes.paper} variant="outlined">
        <Typography variant="subtitle1" color="inherit">
          {props.ip}
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
      </Paper> */}
      <ExpansionPanel>
        <ExpansionPanelSummary
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel1a-content"
          id="panel1a-header"
        >
          <Typography className={classes.heading}>{props.ip}</Typography>
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
