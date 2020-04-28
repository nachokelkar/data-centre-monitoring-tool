import React, { useCallback, useEffect, useState } from "react";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import CardHeader from "@material-ui/core/CardHeader";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/core/styles";
import Container from "@material-ui/core/Container";
import Server from "./Server";

const useStyles = makeStyles((theme) => ({
    "@global": {
        ul: {
            margin: 0,
            padding: 0,
            listStyle: "none",
        },
    },
    heroContent: {
        padding: theme.spacing(8, 0, 6),
    },
    cardHeader: {
        backgroundColor:
            theme.palette.type === "dark"
                ? theme.palette.grey[700]
                : theme.palette.grey[200],
    },
}));

export default function Racks() {
    const classes = useStyles();
    const [racks, setRacks] = useState([]);

    const fetchSnmp = useCallback(async () => {
        let res = await fetch("http://127.0.0.1:5000/api/v1/snmp", {
            mode: "cors",
            headers: {
                "Content-Type": "application/json",
            },
        }).catch((e) => alert("Network Error"));
        let data = await res.json();
        let tmp_rack1 = [];
        let tmp_rack2 = [];
        let tmp_rack3 = [];
        for (var ip in data) {
            //get ping & ssh data here, append to each data[ip]
            let pingRes = await fetch(
                "http://127.0.0.1:5000/api/v1/ping/" + ip,
                {
                    mode: "cors",
                    headers: {
                        "Content-Type": "application/json",
                    },
                }
            ).catch((e) => alert("Network Error"));
            let pingData = await pingRes.json();
            pingData = pingData.data;
            let serverStatus;
            if (pingData === "True") serverStatus = "OK";
            else serverStatus = "NOK";

            data[ip].push(serverStatus);
            // Rack 1
            if (data[ip][0] === "1") {
                let server = {};
                server[ip] = data[ip];
                tmp_rack1.push(server);
            }
            // Rack 2
            else if (data[ip][0] === "2") {
                let server = { ip: data[ip] };
                tmp_rack2.push(server);
            }
            // Rack 3
            else if (data[ip][0] === "3") {
                let server = { ip: data[ip] };
                tmp_rack3.push(server);
            }
        }

        /* dummy data code */
        tmp_rack1.push({
            "17.192.60.49": [
                "1",
                "22",
                "45",
                "51",
                "Windows 10",
                "895082",
                "OK",
            ],
        });
        tmp_rack1.push({
            "235.206.163.213": [
                "1",
                "24",
                "41",
                "91",
                "CentOS",
                "845082",
                "OK",
            ],
        });
        tmp_rack1.push({
            "31.48.70.92": ["1", "34", "15", "71", "Ubuntu", "895082", "NOK"],
        });
        tmp_rack2.push({
            "249.8.152.227": ["2", "82", "61", "65", "CentOS", "895082", "OK"],
        });
        tmp_rack2.push({
            "8.220.11.103": [
                "2",
                "82",
                "61",
                "65",
                "Windows 10",
                "895082",
                "OK",
            ],
        });
        tmp_rack2.push({
            "38.192.127.154": ["2", "82", "61", "65", "Ubuntu", "895082", "OK"],
        });
        tmp_rack2.push({
            "22.74.368.15": [
                "2",
                "82",
                "61",
                "65",
                "Windows 10",
                "895082",
                "OK",
            ],
        });
        tmp_rack3.push({
            "106.7.151.150": ["2", "82", "61", "65", "Ubuntu", "895082", "NOK"],
        });
        tmp_rack3.push({
            "174.185.160.163": [
                "2",
                "82",
                "61",
                "65",
                "Windows 10",
                "895082",
                "OK",
            ],
        });
        tmp_rack3.push({
            "212.74.38.159": ["2", "82", "61", "65", "Ubuntu", "895082", "OK"],
        });

        /* end of dummy data code*/

        let tmp_racks = [];
        tmp_racks.push(tmp_rack1);
        tmp_racks.push(tmp_rack2);
        tmp_racks.push(tmp_rack3);
        console.log(tmp_racks);
        setRacks(tmp_racks);
    }, []);

    useEffect(() => {
        fetchSnmp();
        setInterval(() => {
            fetchSnmp();
        }, 5000);
    }, [fetchSnmp]);
    return (
        <React.Fragment>
            {/* Hero unit */}
            <Container
                maxWidth="sm"
                component="main"
                className={classes.heroContent}
            >
                <Typography
                    component="h1"
                    variant="h2"
                    align="center"
                    color="textPrimary"
                    gutterBottom
                >
                    Data Center
                </Typography>
            </Container>
            {/* End hero unit */}
            <Container maxWidth="lg" component="main">
                <Grid container spacing={2}>
                    {racks.map((rack) => {
                        let i = 1;
                        let title = "Rack " + i;
                        i = i + 1;
                        return (
                            <Grid item xs={12} md={4}>
                                <Card>
                                    <CardHeader
                                        title={title}
                                        titleTypographyProps={{
                                            align: "center",
                                        }}
                                        subheaderTypographyProps={{
                                            align: "center",
                                        }}
                                        className={classes.cardHeader}
                                    />
                                    <CardContent>
                                        <ul>
                                            {rack.map((server) => {
                                                let pos = 0;
                                                let ip = Object.keys(server)[0];
                                                pos = pos + 1;
                                                let entries = server[ip];
                                                return (
                                                    <React.Fragment>
                                                        <Server
                                                            // expanded={true}
                                                            position={pos}
                                                            ip={ip}
                                                            os={entries[4]}
                                                            cpu={entries[1]}
                                                            dsk={entries[2]}
                                                            ok={entries[6]}
                                                        />
                                                    </React.Fragment>
                                                );
                                            })}
                                        </ul>
                                    </CardContent>
                                </Card>
                            </Grid>
                        );
                    })}
                </Grid>
            </Container>
        </React.Fragment>
    );
}
