import React, { useState } from "react";
import {
      Text,
      View,
      Picker,
      StyleSheet,
      TextInput,
      Button,
      Alert,
      Platform,Pressable
} from "react-native";
import { useForm, Controller } from "react-hook-form";
import Constants from "expo-constants";
import DateTimePicker from "@react-native-community/datetimepicker";


const MedicationScreen = () => {
      const [date, setDate] = useState(new Date());
      const [mode, setMode] = useState("date");
      const [show, setShow] = useState(false);
      const [text, setText] = useState("Select start date and time");

      const {
            register,
            setValue,
            handleSubmit,
            control,
            reset,
            formState: { errors },
      } = useForm({
            defaultValues: {
                  medicineName: "",
                  days: ""
            },
      });

      const onChange = (event, selectedDate) => {
            const currentDate = selectedDate || date;
            setShow(Platform.OS === "ios");
            setDate(currentDate);

            let tempDate = new Date(currentDate);
            let fDate = tempDate.getDate() + "/" + (tempDate.getMonth()+1) + "/" + tempDate.getFullYear();
            let fTime = " Hours : " + tempDate.getHours() + ' | Minutes : '+ tempDate.getMinutes();
            setText(' Starting Date : '+fDate+'\n'+' Starting Time : '+fTime)
      };

      const showMode = (currentMode) => {
            setShow(true);
            setMode(currentMode);
      };

      const showDatepicker = () => {
            showMode("date");
      };

      const showTimepicker = () => {
            showMode("time");
      };

      // var gapi = window.gapi
      // var CLIENT_ID = "116996169600907890900"
      // var API_KEY = "8552f64ae8e5ed0b6dde6f39775b59b149f13bd4"
      // var DISCOVERY_DOCS = ["https://www.googleapis.com/discovery/v1/apis/calendar/v3/rest"]
      // var SCOPES = "https://www.googleapis.com/auth/calendar.events"
    
      const handleClick = () => {
        gapi.load('client:auth2', () => {
          console.log('loaded client')
    
          gapi.client.init({
            apiKey: API_KEY,
            clientId: CLIENT_ID,
            discoveryDocs: DISCOVERY_DOCS,
            scope: SCOPES,
          })
    
         
    
          gapi.auth2.getAuthInstance().signIn()
      //     .then(() => {
            
      //       var event = {
      //         'summary': 'Awesome Event!',
      //         'location': '800 Howard St., San Francisco, CA 94103',
      //         'description': 'Really great refreshments',
      //         'start': {
      //           'dateTime': '2022-03-13T09:00:00-07:00',
      //           'timeZone': 'America/Los_Angeles'
      //         },
      //         'end': {
      //           'dateTime': '2022-03-14T17:00:00-07:00',
      //           'timeZone': 'America/Los_Angeles'
      //         },
      //         'recurrence': [
      //           'RRULE:FREQ=DAILY;COUNT=2'
      //         ],
      //         'attendees': [
      //           {'email': 'lpage@example.com'},
      //           {'email': 'sbrin@example.com'}
      //         ],
      //         'reminders': {
      //           'useDefault': false,
      //           'overrides': [
      //             {'method': 'email', 'minutes': 24 * 60},
      //             {'method': 'popup', 'minutes': 10}
      //           ]
      //         }
      //       }
    
      //       var request = gapi.client.calendar.events.insert({
      //         'calendarId': 'primary',
      //         'resource': event,
      //       })
    
      //       request.execute(event => {
      //         console.log(event)
      //         window.open(event.htmlLink)
      //       })
            
    
      //       /*
      //           Uncomment the following block to get events
      //       */
      //       /*
      //       // get events
      //       gapi.client.calendar.events.list({
      //         'calendarId': 'primary',
      //         'timeMin': (new Date()).toISOString(),
      //         'showDeleted': false,
      //         'singleEvents': true,
      //         'maxResults': 10,
      //         'orderBy': 'startTime'
      //       }).then(response => {
      //         const events = response.result.items
      //         console.log('EVENTS: ', events)
      //       })
      //       */
        
    
      //     })
        })
      }
    
      return (
            <View style={styles.container}>
                  <Text style={styles.label}>Medicine Name</Text>
                  <Controller
                        control={control}
                        render={({ field: { onChange, onBlur, value } }) => (
                              <TextInput
                                    style={styles.input}
                                    onBlur={onBlur}
                                    onChangeText={(value) => onChange(value)}
                                    value={value}
                              />
                        )}
                        name="medicineName"
                        rules={{ required: true }}
                  />
                  <Text style={styles.label}>No. of Days</Text>
                  <Controller
                        control={control}
                        render={({ field: { onChange, onBlur, value } }) => (
                              <TextInput
                                    style={styles.input}
                                    onBlur={onBlur}
                                    onChangeText={(value) => onChange(value)}
                                    value={value}
                              />
                        )}
                        name="days"
                        rules={{ required: true }}
                  />
                  <Text style={styles.text}>{text}</Text>
                  <Pressable
                                    onPress={showDatepicker}
                                    title="Choose start date"
                                    style={styles.button}
                              >
                                   <Text style={styles.text}>Choose start date</Text>
                                   </Pressable>
                    <Pressable
                                    onPress={showTimepicker}
                                    title="Choose start time"
                                    style={styles.button}
                              >
                                   <Text style={styles.text}>Choose start time</Text>
                                   </Pressable>
                              {show && (
                              <DateTimePicker
                                    testID="dateTimePicker"
                                    value={date}
                                    mode={mode}
                                    is24Hour={true}
                                    display="default"
                                    onChange={onChange}
                              />
                        )}
                  <View style={styles.button}>
                        <Pressable
                              title="Submit"
                              onPress={handleClick}
                        >
                             <Text style={styles.text}>Submit</Text>
                             </Pressable>
                  </View>
            </View>
      );
};

export default MedicationScreen;

const styles = StyleSheet.create({
      label: {
            color: "black",
            marginLeft: 0,
            marginBottom: 10,
            fontSize: 16,
          lineHeight: 21,
          fontWeight: 'bold',
          letterSpacing: 0.25,
      },
      button: {
          alignItems: 'center',
          justifyContent: 'center',
          paddingVertical: 12,
          paddingHorizontal: 32,
          borderRadius: 4,
          elevation: 3,
          backgroundColor: '#2FA4FF',
          margin:30
        },
      container: {
            flex: 1,
            justifyContent: "center",
            paddingTop: Constants.statusBarHeight,
            padding: 8,
            backgroundColor: "#E8FFC2",
      },
      input: {
            backgroundColor: "#2FA4FF",
            borderColor: "black",
            height: 40,
            padding: 10,
            borderRadius: 4,
            color: "white",
            fontSize: 15,
            marginBottom:40
      },
      text: {
          fontSize: 16,
          lineHeight: 21,
          fontWeight: 'bold',
          letterSpacing: 0.25,
          color: 'black',
        }
});
