import React, { useState } from "react";
import Paper from "@material-ui/core/Paper";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import { PieChart, Pie, Sector } from "recharts";
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
        // height: 520,
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
    info: {
        background: "#3e3e3e",
        color: "white",
        padding: theme.spacing(2),
        marginTop: theme.spacing(3),
        width: 300,
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

    const [activeIndex] = useState(0);
    const cpuData = [
        { name: "CPU", value: Number(props.cpu) },
        { name: "Idle%", value: Number(100 - props.cpu) },
    ];
    const dskData = [
        { name: "Disk", value: Number(props.dsk) },
        { name: "Idle%", value: Number(100 - props.dsk) },
    ];

    const renderActiveShape = (props) => {
        const RADIAN = Math.PI / 180;
        const {
            cx,
            cy,
            midAngle,
            innerRadius,
            outerRadius,
            startAngle,
            endAngle,
            fill,
            payload,
            percent,
            // value,
        } = props;
        const sin = Math.sin(-RADIAN * midAngle);
        const cos = Math.cos(-RADIAN * midAngle);
        const sx = cx + (outerRadius + 10) * cos;
        const sy = cy + (outerRadius + 10) * sin;
        const mx = cx + (outerRadius + 30) * cos;
        const my = cy + (outerRadius + 30) * sin;
        const ex = mx + (cos >= 0 ? 1 : -1) * 22;
        const ey = my;
        const textAnchor = cos >= 0 ? "start" : "end";

        return (
            <g>
                <text x={cx} y={cy} dy={8} textAnchor="middle" fill={fill}>
                    {payload.name}
                </text>
                <Sector
                    cx={cx}
                    cy={cy}
                    innerRadius={innerRadius}
                    outerRadius={outerRadius}
                    startAngle={startAngle}
                    endAngle={endAngle}
                    fill={fill}
                />
                <Sector
                    cx={cx}
                    cy={cy}
                    startAngle={startAngle}
                    endAngle={endAngle}
                    innerRadius={outerRadius + 6}
                    outerRadius={outerRadius + 10}
                    fill={fill}
                />
                <path
                    d={`M${sx},${sy}L${mx},${my}L${ex},${ey}`}
                    stroke={fill}
                    fill="none"
                />
                <circle cx={ex} cy={ey} r={2} fill={fill} stroke="none" />
                <text
                    x={ex + (cos >= 0 ? 1 : -1) * 12}
                    y={ey}
                    textAnchor={textAnchor}
                    fill="#373"
                >{`Usage`}</text>
                <text
                    x={ex + (cos >= 0 ? 1 : -1) * 12}
                    y={ey}
                    dy={18}
                    textAnchor={textAnchor}
                    fill="#999"
                >
                    {`(${(percent * 100).toFixed(2)}%)`}
                </text>
            </g>
        );
    };

    return (
        <Dialog
            onClose={handleClose}
            aria-labelledby="simple-dialog-title"
            open={open}
        >
            <DialogTitle id="simple-dialog-title">
                Server Info ({props.ip})
            </DialogTitle>
            <Paper className={classes.paper}>
                {/* <Grid item xs={12}>
                    <Typography variant="h6" className={classes.paperHeading}>
                        IP Address: {props.ip}
                    </Typography>
                </Grid> */}
                <Grid item xs={12}>
                    {/* <Typography variant="subtitle1" className={classes.metrics}>
                        CPU(%): {props.cpu}
                    </Typography> */}
                    <PieChart width={600} height={150}>
                        <Pie
                            activeIndex={activeIndex}
                            activeShape={renderActiveShape}
                            data={cpuData}
                            cx={200}
                            cy={100}
                            innerRadius={30}
                            outerRadius={40}
                            fill="#8894F8"
                            dataKey="value"
                        />
                    </PieChart>
                </Grid>
                <Grid item xs={12}>
                    {/* <Typography variant="subtitle1" className={classes.metrics}>
                        Disk(%): {props.dsk}
                    </Typography> */}
                    <Grid item xs={12}>
                        <PieChart width={600} height={200}>
                            <Pie
                                activeIndex={activeIndex}
                                activeShape={renderActiveShape}
                                data={dskData}
                                cx={200}
                                cy={100}
                                innerRadius={30}
                                outerRadius={40}
                                fill="#8894F8"
                                dataKey="value"
                            />
                        </PieChart>
                    </Grid>
                </Grid>
                <Grid item xs={12}>
                    <Paper className={classes.info}>
                        <Typography
                            variant="subtitle1"
                            className={classes.metrics}
                        >
                            Ping Status:
                            <Typography
                                variant="h6"
                                className={classes.metrics}
                                color={props.ping==="OK" ? "secondary" : "error"}
                            >
                                {props.ping}
                            </Typography>
                        </Typography>
                        {/* <Typography
                            variant="subtitle1"
                            className={classes.metrics}
                        >
                            Uptime: {props.upt} s
                        </Typography> */}
                    </Paper>
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
