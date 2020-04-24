import React from "react";
import Paper from "@material-ui/core/Paper";
import Grid from "@material-ui/core/Grid";
import DialogTitle from "@material-ui/core/DialogTitle";
import Dialog from "@material-ui/core/Dialog";
import IconButton from "@material-ui/core/IconButton";
import OpenInNewOutlined from "@material-ui/icons/OpenInNewOutlined";
import ExpansionPanel from "@material-ui/core/ExpansionPanel";
import ExpansionPanelDetails from "@material-ui/core/ExpansionPanelDetails";
import ExpansionPanelSummary from "@material-ui/core/ExpansionPanelSummary";
import Typography from "@material-ui/core/Typography";
import ExpandMoreIcon from "@material-ui/icons/ExpandMore";
import CheckOutlinedIcon from "@material-ui/icons/CheckOutlined";
import CloseOutlinedIcon from "@material-ui/icons/CloseOutlined";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({
    paper: {
        background: "#3e3e3e",
        color: "white",
        height: 120,
        width: 335,
        paddingTop: theme.spacing(1),
        paddingLeft: theme.spacing(2),
        marginBottom: theme.spacing(2),
    },
    position: {
        paddingRight: theme.spacing(3),
    },
    margin: {
        color: "white",
        paddingRight: theme.spacing(1),
        paddingBottom: theme.spacing(1),
        paddingLeft: theme.spacing(1),
        paddingTop: theme.spacing(0),
        marginTop: theme.spacing(0),
    },
}));

function SimpleDialog(props) {
    // const classes = useStyles();
    const { onClose, selectedValue, open } = props;

    const handleClose = () => {
        onClose(selectedValue);
    };

    // const handleListItemClick = value => {
    //   onClose(value);
    // };

    return (
        <Dialog
            onClose={handleClose}
            aria-labelledby="simple-dialog-title"
            open={open}
        >
            <DialogTitle id="simple-dialog-title">
                Network Topology {"&"} Other Info
            </DialogTitle>
            <Paper>
                -Network Topology
                <br /> -ssh info
            </Paper>
        </Dialog>
    );
}

export default function Racks(props) {
    const classes = useStyles();
    const [open, setOpen] = React.useState(false);
    const serverStatus = props.ok === "OK" ? true : false;
    const selectedValue = React.useState(true);

    const handleClickOpen = () => {
        setOpen(true);
    };

    const handleClose = (value) => {
        setOpen(false);
    };
    return (
        <React.Fragment>
            <ExpansionPanel expanded={props.expanded}>
                <ExpansionPanelSummary
                    expandIcon={<ExpandMoreIcon />}
                    aria-controls="panel1a-content"
                    id="panel1a-header"
                >
                    <Grid item xs={1}>
                        <Typography
                            variant="subtitle1"
                            className={classes.position}
                        >
                            {props.position}.
                        </Typography>
                    </Grid>

                    <Grid item xs={9}>
                        <Typography variant="subtitle1">{props.ip}</Typography>
                    </Grid>

                    <Grid item xs={1}>
                        {serverStatus ? (
                            <CheckOutlinedIcon
                                color="secondary"
                                fontSize="small"
                            />
                        ) : (
                            <CloseOutlinedIcon color="error" fontSize="small" />
                        )}
                    </Grid>
                </ExpansionPanelSummary>
                <ExpansionPanelDetails>
                    <Paper className={classes.paper} variant="outlined">
                        <Grid container>
                            <Grid item xs={10}>
                                <Typography variant="caption" color="inherit">
                                    {props.os}
                                </Typography>
                            </Grid>
                            <Grid item xs={2}>
                                <IconButton
                                    aria-label="open"
                                    className={classes.margin}
                                    onClick={handleClickOpen}
                                >
                                    <OpenInNewOutlined fontSize="small" />
                                </IconButton>
                            </Grid>
                        </Grid>
                        <Grid container>
                            <Grid item xs={3}>
                                <Typography variant="caption" color="inherit">
                                    CPU(%)
                                </Typography>
                                <Typography variant="h6">
                                    {" "}
                                    {props.cpu}{" "}
                                </Typography>
                            </Grid>
                            <Grid item xs={6}>
                                <Typography variant="caption" color="inherit">
                                    Disk Usage(%)
                                </Typography>
                                <Typography variant="h6">
                                    {" "}
                                    {props.dsk}{" "}
                                </Typography>
                            </Grid>
                            <Grid item xs={3}>
                                <Typography variant="caption" color="inherit">
                                    Status
                                </Typography>
                                <Typography
                                    variant={serverStatus ? "h6" : "caption"}
                                    color={serverStatus ? "secondary" : "error"}
                                >
                                    {" "}
                                    {serverStatus
                                        ? "OK"
                                        : "Needs Attention"}{" "}
                                </Typography>
                            </Grid>
                        </Grid>
                    </Paper>
                </ExpansionPanelDetails>
            </ExpansionPanel>
            <SimpleDialog
                selectedValue={selectedValue}
                open={open}
                onClose={handleClose}
            />
        </React.Fragment>
    );
}
