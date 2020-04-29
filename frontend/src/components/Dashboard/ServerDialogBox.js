import React, { useState } from "react";
import Paper from "@material-ui/core/Paper";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import ListItemIcon from "@material-ui/core/ListItemIcon";
import ListItemText from "@material-ui/core/ListItemText";
import DialogTitle from "@material-ui/core/DialogTitle";
import Dialog from "@material-ui/core/Dialog";
import PersonIcon from "@material-ui/icons/Person";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({
    paper: {
        height: 520,
        width: 535,
        paddingTop: theme.spacing(0),
        paddingLeft: theme.spacing(2),
        // marginBottom: theme.spacing(2),
    },
    paperHeading: {
        paddingRight: theme.spacing(1),
        paddingBottom: theme.spacing(1),
        // paddingLeft: theme.spacing(3),
        paddingTop: theme.spacing(3),
        marginTop: theme.spacing(0),
    },
    metrics: {
        paddingLeft: theme.spacing(3),
    },
}));

export default function SimpleDialog(props) {
    const classes = useStyles();
    const { onClose, selectedValue, open } = props;

    const [users, setUsers] = useState([]);
    const [hasFetchedUsers, setHasFetchedUsers] = useState(false);

    const lastLoggedIn = async () => {
        let res = await fetch("http://127.0.0.1:5000/api/v1/ssh/" + props.ip, {
            mode: "cors",
            headers: {
                "Content-Type": "application/json",
            },
        }).catch((e) => alert("Network Error"));
        let data = await res.json();

        let tmpUsers;
        if (data[props.ip] !== undefined) {
            tmpUsers = data[props.ip].last;
            tmpUsers = tmpUsers.split("\n");
            setUsers(tmpUsers);
            setHasFetchedUsers(true);
        }
    };

    if (!hasFetchedUsers) lastLoggedIn();

    const handleClose = () => {
        onClose(selectedValue);
    };

    return (
        <Dialog
            onClose={handleClose}
            aria-labelledby="simple-dialog-title"
            open={open}
        >
            <DialogTitle id="simple-dialog-title">Server Info</DialogTitle>
            <Paper className={classes.paper}>
                <Grid item xs={12}>
                    <Typography variant="h6" className={classes.paperHeading}>
                        IP Address: {props.ip}
                    </Typography>
                </Grid>
                <Grid item xs={12}>
                    <Typography variant="subtitle1" className={classes.metrics}>
                        CPU(%): {props.cpu}
                    </Typography>
                </Grid>
                <Grid item xs={12}>
                    <Typography variant="subtitle1" className={classes.metrics}>
                        Disk(%): {props.dsk}
                    </Typography>
                </Grid>
                <Grid item xs={12}>
                    <Typography variant="subtitle1" className={classes.metrics}>
                        Ping Status(%): {props.ping}
                    </Typography>
                </Grid>
                {hasFetchedUsers ? (
                    <Grid item>
                        <Typography
                            variant="h6"
                            className={classes.paperHeading}
                        >
                            Last logged in users list
                        </Typography>
                        <List component="nav" aria-label="main mailbox folders">
                            {users.map((user) => (
                                <ListItem>
                                    <ListItemIcon>
                                        <PersonIcon fontSize="small" />
                                    </ListItemIcon>
                                    <ListItemText primary={user} />
                                </ListItem>
                            ))}
                        </List>
                    </Grid>
                ) : (
                    <></>
                )}
            </Paper>
        </Dialog>
    );
}
