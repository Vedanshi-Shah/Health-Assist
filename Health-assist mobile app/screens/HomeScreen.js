import React from "react";
import {
    SafeAreaView,
    View,
    Text,
    Image,
    FlatList,
    TouchableOpacity,
    StyleSheet,
    LogBox,
    KeyboardAvoidingView
} from "react-native"
import { COLORS, SIZES, FONTS, icons, images } from "../constants"
import * as Linking from 'expo-linking';
import { useNavigation } from '@react-navigation/core'

const HomeScreen = () => {

  const navigation = useNavigation()

    LogBox.ignoreLogs(["Warning:"]);
    const getBotUpdates = () =>
  fetch(
    "https://api.telegram.org/bot5269408453:AAE_RBXbkenl8ucm5dviP0Nmj3utQa5t5gE/getUpdates"
  ).then((response) => response.json());

    const handleBot=()=>{
      // fetch(
      //   "https://t.me/HealthAssistancebot?start=/start"
      // ).then((response) => response.json());
     
      Linking.openURL('https://t.me/HealthAssistancebot?start=/start');
    }
    
    const medication=()=>{
    
      navigation.navigate("Medication")
    }
    const specialPromoData = [
        {
            id: 1,
            img: images.physicalhealth,
            title: "Physical Health Chat Bot",
            description: "Click here to chat"
        },
        {
            id: 2,
            img: images.mentalhealth,
            title: "Mental Health Chat Bot",
            description: "Click here to chat"
        },
        {
            id: 3,
            img: images.reminder,
            title: "Medication Reminder",
            description: "Click here to set medication reminders"
        },
        {
            id: 4,
            img: images.pharmacy,
            title: "Nearby Pharmacies",
            description: "Click here to find pharmacies nearby you"
        },
    ]
    const [specialPromos, setSpecialPromos] = React.useState(specialPromoData)

    function renderBanner() {
      return (
          <View
              style={{
                  height: 100,
                  borderRadius: 15,
              }}
          >
              <Image
                  source={images.wallieLogo}
                  resizeMode="contain"
                  style={{
                      width: "100%",
                      height: "100%",
                      borderRadius: 20
                  }}
              />
          </View>
      )
  }


    function renderPromos() {

        const HeaderComponent = () => (
            <View>
                <View style={{ flexDirection: 'row', marginVertical: SIZES.padding * 2 }}></View>
                {renderBanner()}
                {renderPromoHeader()}
            </View>
        )

        const renderPromoHeader = () => (
            <View
                style={{
                    flexDirection: 'row',
                    marginBottom: SIZES.padding,
                    marginTop:10
                }}
            >
                <View style={{ flex: 1 }}>
                    <Text style={{ ...FONTS.h3 }} >Healthcare Assistant !</Text>
                </View>
            </View>

        )

        const renderItem = ({ item }) => (
            <TouchableOpacity
                style={{
                    marginVertical: SIZES.base,
                    width: SIZES.width / 2.5
                }}
                onPress={()=>{
                    if(item.title==="Physical Health Chat Bot"){
                        Linking.openURL('https://t.me/HealthAssistancebot?start=/start');
                    }
                    else if(item.title==="Mental Health Chat Bot"){
                        Linking.openURL('https://t.me/mentalchat_bot?start=/start');
                    }
                    else if(item.title==="Medication Reminder"){
                        navigation.navigate("Medication");
                    }

                }}
            >
                <View
                    style={{
                        height: 80,
                        borderTopLeftRadius: 20,
                        borderTopRightRadius: 20,
                        backgroundColor: COLORS.primary
                    }}
                >
                    <Image
                        source={item.img}
                        resizeMode="contain"
                        style={{
                            width: "100%",
                            height: "100%",
                            borderTopLeftRadius: 20,
                            borderTopRightRadius: 20
                        }}
                    />
                </View>

                <View
                    style={{
                        padding: SIZES.padding,
                        backgroundColor: COLORS.lightGray,
                        borderBottomLeftRadius: 20,
                        borderBottomRightRadius: 20
                    }}
                >
                    <Text style={{ ...FONTS.h4 }}>{item.title}</Text>
                    <Text style={{ ...FONTS.body4 }}>{item.description}</Text>
                </View>
            </TouchableOpacity>
        )

        return (
            <FlatList
                ListHeaderComponent={HeaderComponent}
                contentContainerStyle={{ paddingHorizontal: SIZES.padding * 3 }}
                numColumns={2}
                columnWrapperStyle={{ justifyContent: 'space-between' }}
                data={specialPromos}
                keyExtractor={item => `${item.id}`}
                renderItem={renderItem}
                showsVerticalScrollIndicator={false}
                ListFooterComponent={
                    <View style={{ marginBottom: 80 }}>
                    </View>
                }
            />
        )
    }

    return (
        <SafeAreaView style={{ flex: 1, backgroundColor: COLORS.yellow }}>
            {renderPromos()}
        </SafeAreaView>
    )
}

export default HomeScreen;