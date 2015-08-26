import re, pytz, datetime, time
from pytz import timezone
from datetime import timedelta, tzinfo

ruby='''<zone id="Etc/GMT+12" name="[GMT -12:00] Eniwetok, Kwaialein" offset="-43200000" />
	<zone id="Pacific/Niue" name="[GMT -11:00] Midway Island, Samoa" offset="-39600000" />
	<zone id="Pacific/Honolulu" name="[GMT -10:00] Hawaii" offset="-36000000" />
	<zone id="America/Anchorage" name="[GMT -09:00] Alaska" offset="-28800000" />
	<zone id="America/Vancouver" name="[GMT -08:00] Pacific Time (USA &amp; Canada)" offset="-25200000" />
	<zone id="America/Edmonton" name="[GMT -07:00] Mountain Time (USA &amp; Canada)" offset="-21600000" />
	<zone id="America/Chicago" name="[GMT -06:00] Central Time (USA &amp; Canada)" offset="-18000000" />
	<zone id="America/Montreal" name="[GMT -05:00] Eastern Time (USA &amp; Canada)" offset="-14400000" />
	<zone id="America/Halifax" name="[GMT -04:00] Atlantic Time (USA &amp; Canada)" offset="-10800000" />
	<zone id="America/Argentina/Buenos_Aires" name="[GMT -03:00] Brasilia" offset="-10800000" />
	<zone id="Atlantic/South_Georgia" name="[GMT -02:00] Mid-Atlantic" offset="-7200000" />
	<zone id="Atlantic/Azores" name="[GMT -01:00] Azores, Cape Verde Is." offset="0" />
	<zone id="Europe/London" name="[GMT +00:00] Greenwich Mean Time" offset="3600000" />
	<zone id="Europe/Amsterdam" name="[GMT +01:00] Amsterdam, Budapest, Madrid, Paris, Warsaw" offset="7200000" />
	<zone id="Europe/Helsinki" name="[GMT +02:00] Athens, Cairo, Helsinki, Israel" offset="10800000" />
	<zone id="Europe/Moscow" name="[GMT +04:00] Baghdad, Moscow, St. Petersburg" offset="14400000" />
	<zone id="Asia/Dubai" name="[GMT +04:00] Abu Dhabi, Tblisi" offset="14400000" />
	<zone id="Asia/Karachi" name="[GMT +05:00] Islamabad, Karachi" offset="18000000" />
	<zone id="Asia/Colombo" name="[GMT +05:30] Bombay, Madras, New Delhi, Colombo" offset="19800000" />
	<zone id="Asia/Almaty" name="[GMT +06:00] Almaty, Dhaka" offset="21600000" />
	<zone id="Asia/Bangkok" name="[GMT +07:00] Bangkok, Hanoi, Jakarta" offset="25200000" />
	<zone id="Asia/Hong_Kong" name="[GMT +08:00] Beijing, Hong Kong, Perth, Singapore, Taipei" offset="28800000" />
	<zone id="Asia/Tokyo" name="[GMT +09:00] Osaka, Tokyo, Seoul" offset="32400000" />
	<zone id="Australia/Adelaide" name="[GMT +09:30] Adelaide, Darwin" offset="34200000" />
	<zone id="Australia/Brisbane" name="[GMT +10:00] Brisbane, Melbourne, Sydney" offset="36000000" />
	<zone id="Pacific/Pohnpei" name="[GMT +11:00] Solomon Islands" offset="39600000" />
	<zone id="Pacific/Auckland" name="[GMT +12:00] Auckland, Fiji, Wellington" offset="43200000" />'''

sbm='''<zone id="Africa/Abidjan" name="[GMT +00:00] Africa/Abidjan" offset="0" />
	<zone id="Africa/Accra" name="[GMT +00:00] Africa/Accra" offset="0" />
	<zone id="Africa/Addis_Ababa" name="[GMT +03:00] Africa/Addis Ababa" offset="10800000" />
	<zone id="Africa/Algiers" name="[GMT +01:00] Africa/Algiers" offset="3600000" />
	<zone id="Africa/Asmara" name="[GMT +03:00] Africa/Asmara" offset="10800000" />
	<zone id="Africa/Bamako" name="[GMT +00:00] Africa/Bamako" offset="0" />
	<zone id="Africa/Bangui" name="[GMT +01:00] Africa/Bangui" offset="3600000" />
	<zone id="Africa/Banjul" name="[GMT +00:00] Africa/Banjul" offset="0" />
	<zone id="Africa/Bissau" name="[GMT +00:00] Africa/Bissau" offset="0" />
	<zone id="Africa/Blantyre" name="[GMT +02:00] Africa/Blantyre" offset="7200000" />
	<zone id="Africa/Brazzaville" name="[GMT +01:00] Africa/Brazzaville" offset="3600000" />
	<zone id="Africa/Bujumbura" name="[GMT +02:00] Africa/Bujumbura" offset="7200000" />
	<zone id="Africa/Cairo" name="[GMT +02:00] Africa/Cairo" offset="7200000" />
	<zone id="Africa/Casablanca" name="[GMT +00:00] Africa/Casablanca" offset="3600000" />
	<zone id="Africa/Ceuta" name="[GMT +01:00] Africa/Ceuta" offset="7200000" />
	<zone id="Africa/Conakry" name="[GMT +00:00] Africa/Conakry" offset="0" />
	<zone id="Africa/Dakar" name="[GMT +00:00] Africa/Dakar" offset="0" />
	<zone id="Africa/Dar_es_Salaam" name="[GMT +03:00] Africa/Dar es Salaam" offset="10800000" />
	<zone id="Africa/Djibouti" name="[GMT +03:00] Africa/Djibouti" offset="10800000" />
	<zone id="Africa/Douala" name="[GMT +01:00] Africa/Douala" offset="3600000" />
	<zone id="Africa/El_Aaiun" name="[GMT +00:00] Africa/El Aaiun" offset="0" />
	<zone id="Africa/Freetown" name="[GMT +00:00] Africa/Freetown" offset="0" />
	<zone id="Africa/Gaborone" name="[GMT +02:00] Africa/Gaborone" offset="7200000" />
	<zone id="Africa/Harare" name="[GMT +02:00] Africa/Harare" offset="7200000" />
	<zone id="Africa/Johannesburg" name="[GMT +02:00] Africa/Johannesburg" offset="7200000" />
	<zone id="Africa/Juba" name="[GMT +03:00] Africa/Juba" offset="10800000" />
	<zone id="Africa/Kampala" name="[GMT +03:00] Africa/Kampala" offset="10800000" />
	<zone id="Africa/Khartoum" name="[GMT +03:00] Africa/Khartoum" offset="10800000" />
	<zone id="Africa/Kigali" name="[GMT +02:00] Africa/Kigali" offset="7200000" />
	<zone id="Africa/Kinshasa" name="[GMT +01:00] Africa/Kinshasa" offset="3600000" />
	<zone id="Africa/Lagos" name="[GMT +01:00] Africa/Lagos" offset="3600000" />
	<zone id="Africa/Libreville" name="[GMT +01:00] Africa/Libreville" offset="3600000" />
	<zone id="Africa/Lome" name="[GMT +00:00] Africa/Lome" offset="0" />
	<zone id="Africa/Luanda" name="[GMT +01:00] Africa/Luanda" offset="3600000" />
	<zone id="Africa/Lubumbashi" name="[GMT +02:00] Africa/Lubumbashi" offset="7200000" />
	<zone id="Africa/Lusaka" name="[GMT +02:00] Africa/Lusaka" offset="7200000" />
	<zone id="Africa/Malabo" name="[GMT +01:00] Africa/Malabo" offset="3600000" />
	<zone id="Africa/Maputo" name="[GMT +02:00] Africa/Maputo" offset="7200000" />
	<zone id="Africa/Maseru" name="[GMT +02:00] Africa/Maseru" offset="7200000" />
	<zone id="Africa/Mbabane" name="[GMT +02:00] Africa/Mbabane" offset="7200000" />
	<zone id="Africa/Mogadishu" name="[GMT +03:00] Africa/Mogadishu" offset="10800000" />
	<zone id="Africa/Monrovia" name="[GMT +00:00] Africa/Monrovia" offset="0" />
	<zone id="Africa/Nairobi" name="[GMT +03:00] Africa/Nairobi" offset="10800000" />
	<zone id="Africa/Ndjamena" name="[GMT +01:00] Africa/Ndjamena" offset="3600000" />
	<zone id="Africa/Niamey" name="[GMT +01:00] Africa/Niamey" offset="3600000" />
	<zone id="Africa/Nouakchott" name="[GMT +00:00] Africa/Nouakchott" offset="0" />
	<zone id="Africa/Ouagadougou" name="[GMT +00:00] Africa/Ouagadougou" offset="0" />
	<zone id="Africa/Porto-Novo" name="[GMT +01:00] Africa/Porto-Novo" offset="3600000" />
	<zone id="Africa/Sao_Tome" name="[GMT +00:00] Africa/Sao Tome" offset="0" />
	<zone id="Africa/Tripoli" name="[GMT +01:00] Africa/Tripoli" offset="7200000" />
	<zone id="Africa/Tunis" name="[GMT +01:00] Africa/Tunis" offset="3600000" />
	<zone id="Africa/Windhoek" name="[GMT +01:00] Africa/Windhoek" offset="3600000" />
	<zone id="America/Adak" name="[GMT -10:00] America/Adak" offset="-32400000" />
	<zone id="America/Anchorage" name="[GMT -09:00] America/Anchorage" offset="-28800000" />
	<zone id="America/Anguilla" name="[GMT -04:00] America/Anguilla" offset="-14400000" />
	<zone id="America/Antigua" name="[GMT -04:00] America/Antigua" offset="-14400000" />
	<zone id="America/Araguaina" name="[GMT -03:00] America/Araguaina" offset="-10800000" />
	<zone id="America/Argentina/Buenos_Aires" name="[GMT -03:00] America/Argentina/Buenos Aires" offset="-10800000" />
	<zone id="America/Argentina/Catamarca" name="[GMT -03:00] America/Argentina/Catamarca" offset="-10800000" />
	<zone id="America/Argentina/Cordoba" name="[GMT -03:00] America/Argentina/Cordoba" offset="-10800000" />
	<zone id="America/Argentina/Jujuy" name="[GMT -03:00] America/Argentina/Jujuy" offset="-10800000" />
	<zone id="America/Argentina/La_Rioja" name="[GMT -03:00] America/Argentina/La Rioja" offset="-10800000" />
	<zone id="America/Argentina/Mendoza" name="[GMT -03:00] America/Argentina/Mendoza" offset="-10800000" />
	<zone id="America/Argentina/Rio_Gallegos" name="[GMT -03:00] America/Argentina/Rio Gallegos" offset="-10800000" />
	<zone id="America/Argentina/Salta" name="[GMT -03:00] America/Argentina/Salta" offset="-10800000" />
	<zone id="America/Argentina/San_Juan" name="[GMT -03:00] America/Argentina/San Juan" offset="-10800000" />
	<zone id="America/Argentina/San_Luis" name="[GMT -04:00] America/Argentina/San Luis" offset="-10800000" />
	<zone id="America/Argentina/Tucuman" name="[GMT -03:00] America/Argentina/Tucuman" offset="-10800000" />
	<zone id="America/Argentina/Ushuaia" name="[GMT -03:00] America/Argentina/Ushuaia" offset="-10800000" />
	<zone id="America/Aruba" name="[GMT -04:00] America/Aruba" offset="-14400000" />
	<zone id="America/Asuncion" name="[GMT -04:00] America/Asuncion" offset="-14400000" />
	<zone id="America/Atikokan" name="[GMT -05:00] America/Atikokan" offset="-18000000" />
	<zone id="America/Bahia" name="[GMT -03:00] America/Bahia" offset="-10800000" />
	<zone id="America/Bahia_Banderas" name="[GMT -06:00] America/Bahia Banderas" offset="-18000000" />
	<zone id="America/Barbados" name="[GMT -04:00] America/Barbados" offset="-14400000" />
	<zone id="America/Belem" name="[GMT -03:00] America/Belem" offset="-10800000" />
	<zone id="America/Belize" name="[GMT -06:00] America/Belize" offset="-21600000" />
	<zone id="America/Blanc-Sablon" name="[GMT -04:00] America/Blanc-Sablon" offset="-14400000" />
	<zone id="America/Boa_Vista" name="[GMT -04:00] America/Boa Vista" offset="-14400000" />
	<zone id="America/Bogota" name="[GMT -05:00] America/Bogota" offset="-18000000" />
	<zone id="America/Boise" name="[GMT -07:00] America/Boise" offset="-21600000" />
	<zone id="America/Cambridge_Bay" name="[GMT -07:00] America/Cambridge Bay" offset="-21600000" />
	<zone id="America/Campo_Grande" name="[GMT -04:00] America/Campo Grande" offset="-14400000" />
	<zone id="America/Cancun" name="[GMT -06:00] America/Cancun" offset="-18000000" />
	<zone id="America/Caracas" name="[GMT -04:30] America/Caracas" offset="-16200000" />
	<zone id="America/Cayenne" name="[GMT -03:00] America/Cayenne" offset="-10800000" />
	<zone id="America/Cayman" name="[GMT -05:00] America/Cayman" offset="-18000000" />
	<zone id="America/Chicago" name="[GMT -06:00] America/Chicago" offset="-18000000" />
	<zone id="America/Chihuahua" name="[GMT -07:00] America/Chihuahua" offset="-21600000" />
	<zone id="America/Costa_Rica" name="[GMT -06:00] America/Costa Rica" offset="-21600000" />
	<zone id="America/Creston" name="[GMT -07:00] America/Creston" offset="-25200000" />
	<zone id="America/Cuiaba" name="[GMT -04:00] America/Cuiaba" offset="-14400000" />
	<zone id="America/Curacao" name="[GMT -04:00] America/Curacao" offset="-14400000" />
	<zone id="America/Danmarkshavn" name="[GMT +00:00] America/Danmarkshavn" offset="0" />
	<zone id="America/Dawson" name="[GMT -08:00] America/Dawson" offset="-25200000" />
	<zone id="America/Dawson_Creek" name="[GMT -07:00] America/Dawson Creek" offset="-25200000" />
	<zone id="America/Denver" name="[GMT -07:00] America/Denver" offset="-21600000" />
	<zone id="America/Detroit" name="[GMT -05:00] America/Detroit" offset="-14400000" />
	<zone id="America/Dominica" name="[GMT -04:00] America/Dominica" offset="-14400000" />
	<zone id="America/Edmonton" name="[GMT -07:00] America/Edmonton" offset="-21600000" />
	<zone id="America/Eirunepe" name="[GMT -04:00] America/Eirunepe" offset="-14400000" />
	<zone id="America/El_Salvador" name="[GMT -06:00] America/El Salvador" offset="-21600000" />
	<zone id="America/Tijuana" name="[GMT -08:00] America/Tijuana" offset="-25200000" />
	<zone id="America/Indiana/Indianapolis" name="[GMT -05:00] America/Indiana/Indianapolis" offset="-14400000" />
	<zone id="America/Fortaleza" name="[GMT -03:00] America/Fortaleza" offset="-10800000" />
	<zone id="America/Glace_Bay" name="[GMT -04:00] America/Glace Bay" offset="-10800000" />
	<zone id="America/Godthab" name="[GMT -03:00] America/Godthab" offset="-7200000" />
	<zone id="America/Goose_Bay" name="[GMT -04:00] America/Goose Bay" offset="-10800000" />
	<zone id="America/Grand_Turk" name="[GMT -05:00] America/Grand Turk" offset="-14400000" />
	<zone id="America/Grenada" name="[GMT -04:00] America/Grenada" offset="-14400000" />
	<zone id="America/Guadeloupe" name="[GMT -04:00] America/Guadeloupe" offset="-14400000" />
	<zone id="America/Guatemala" name="[GMT -06:00] America/Guatemala" offset="-21600000" />
	<zone id="America/Guayaquil" name="[GMT -05:00] America/Guayaquil" offset="-18000000" />
	<zone id="America/Guyana" name="[GMT -04:00] America/Guyana" offset="-14400000" />
	<zone id="America/Halifax" name="[GMT -04:00] America/Halifax" offset="-10800000" />
	<zone id="America/Havana" name="[GMT -05:00] America/Havana" offset="-14400000" />
	<zone id="America/Hermosillo" name="[GMT -07:00] America/Hermosillo" offset="-25200000" />
	<zone id="America/Indiana/Knox" name="[GMT -06:00] America/Indiana/Knox" offset="-18000000" />
	<zone id="America/Indiana/Marengo" name="[GMT -05:00] America/Indiana/Marengo" offset="-14400000" />
	<zone id="America/Indiana/Petersburg" name="[GMT -05:00] America/Indiana/Petersburg" offset="-14400000" />
	<zone id="America/Indiana/Tell_City" name="[GMT -06:00] America/Indiana/Tell City" offset="-18000000" />
	<zone id="America/Indiana/Vevay" name="[GMT -05:00] America/Indiana/Vevay" offset="-14400000" />
	<zone id="America/Indiana/Vincennes" name="[GMT -05:00] America/Indiana/Vincennes" offset="-14400000" />
	<zone id="America/Indiana/Winamac" name="[GMT -05:00] America/Indiana/Winamac" offset="-14400000" />
	<zone id="America/Inuvik" name="[GMT -07:00] America/Inuvik" offset="-21600000" />
	<zone id="America/Iqaluit" name="[GMT -05:00] America/Iqaluit" offset="-14400000" />
	<zone id="America/Jamaica" name="[GMT -05:00] America/Jamaica" offset="-18000000" />
	<zone id="America/Juneau" name="[GMT -09:00] America/Juneau" offset="-28800000" />
	<zone id="America/Kentucky/Louisville" name="[GMT -05:00] America/Kentucky/Louisville" offset="-14400000" />
	<zone id="America/Kentucky/Monticello" name="[GMT -05:00] America/Kentucky/Monticello" offset="-14400000" />
	<zone id="America/La_Paz" name="[GMT -04:00] America/La Paz" offset="-14400000" />
	<zone id="America/Lima" name="[GMT -05:00] America/Lima" offset="-18000000" />
	<zone id="America/Los_Angeles" name="[GMT -08:00] America/Los Angeles" offset="-25200000" />
	<zone id="America/Maceio" name="[GMT -03:00] America/Maceio" offset="-10800000" />
	<zone id="America/Managua" name="[GMT -06:00] America/Managua" offset="-21600000" />
	<zone id="America/Manaus" name="[GMT -04:00] America/Manaus" offset="-14400000" />
	<zone id="America/Martinique" name="[GMT -04:00] America/Martinique" offset="-14400000" />
	<zone id="America/Matamoros" name="[GMT -06:00] America/Matamoros" offset="-18000000" />
	<zone id="America/Mazatlan" name="[GMT -07:00] America/Mazatlan" offset="-21600000" />
	<zone id="America/Menominee" name="[GMT -06:00] America/Menominee" offset="-18000000" />
	<zone id="America/Merida" name="[GMT -06:00] America/Merida" offset="-18000000" />
	<zone id="America/Metlakatla" name="[GMT -08:00] America/Metlakatla" offset="-28800000" />
	<zone id="America/Mexico_City" name="[GMT -06:00] America/Mexico City" offset="-18000000" />
	<zone id="America/Miquelon" name="[GMT -03:00] America/Miquelon" offset="-7200000" />
	<zone id="America/Moncton" name="[GMT -04:00] America/Moncton" offset="-10800000" />
	<zone id="America/Monterrey" name="[GMT -06:00] America/Monterrey" offset="-18000000" />
	<zone id="America/Montevideo" name="[GMT -03:00] America/Montevideo" offset="-10800000" />
	<zone id="America/Montreal" name="[GMT -05:00] America/Montreal" offset="-14400000" />
	<zone id="America/Montserrat" name="[GMT -04:00] America/Montserrat" offset="-14400000" />
	<zone id="America/Nassau" name="[GMT -05:00] America/Nassau" offset="-14400000" />
	<zone id="America/New_York" name="[GMT -05:00] America/New York" offset="-14400000" />
	<zone id="America/Nipigon" name="[GMT -05:00] America/Nipigon" offset="-14400000" />
	<zone id="America/Nome" name="[GMT -09:00] America/Nome" offset="-28800000" />
	<zone id="America/Noronha" name="[GMT -02:00] America/Noronha" offset="-7200000" />
	<zone id="America/North_Dakota/Beulah" name="[GMT -06:00] America/North Dakota/Beulah" offset="-18000000" />
	<zone id="America/North_Dakota/Center" name="[GMT -06:00] America/North Dakota/Center" offset="-18000000" />
	<zone id="America/North_Dakota/New_Salem" name="[GMT -06:00] America/North Dakota/New Salem" offset="-18000000" />
	<zone id="America/Ojinaga" name="[GMT -07:00] America/Ojinaga" offset="-21600000" />
	<zone id="America/Panama" name="[GMT -05:00] America/Panama" offset="-18000000" />
	<zone id="America/Pangnirtung" name="[GMT -05:00] America/Pangnirtung" offset="-14400000" />
	<zone id="America/Paramaribo" name="[GMT -03:00] America/Paramaribo" offset="-10800000" />
	<zone id="America/Phoenix" name="[GMT -07:00] America/Phoenix" offset="-25200000" />
	<zone id="America/Port-au-Prince" name="[GMT -05:00] America/Port-au-Prince" offset="-14400000" />
	<zone id="America/Port_of_Spain" name="[GMT -04:00] America/Port of Spain" offset="-14400000" />
	<zone id="America/Rio_Branco" name="[GMT -04:00] America/Rio Branco" offset="-14400000" />
	<zone id="America/Porto_Velho" name="[GMT -04:00] America/Porto Velho" offset="-14400000" />
	<zone id="America/Puerto_Rico" name="[GMT -04:00] America/Puerto Rico" offset="-14400000" />
	<zone id="America/Rainy_River" name="[GMT -06:00] America/Rainy River" offset="-18000000" />
	<zone id="America/Rankin_Inlet" name="[GMT -06:00] America/Rankin Inlet" offset="-18000000" />
	<zone id="America/Recife" name="[GMT -03:00] America/Recife" offset="-10800000" />
	<zone id="America/Regina" name="[GMT -06:00] America/Regina" offset="-21600000" />
	<zone id="America/Resolute" name="[GMT -06:00] America/Resolute" offset="-18000000" />
	<zone id="America/Santa_Isabel" name="[GMT -08:00] America/Santa Isabel" offset="-25200000" />
	<zone id="America/Santarem" name="[GMT -03:00] America/Santarem" offset="-10800000" />
	<zone id="America/Santiago" name="[GMT -04:00] America/Santiago" offset="-14400000" />
	<zone id="America/Santo_Domingo" name="[GMT -04:00] America/Santo Domingo" offset="-14400000" />
	<zone id="America/Sao_Paulo" name="[GMT -03:00] America/Sao Paulo" offset="-10800000" />
	<zone id="America/Scoresbysund" name="[GMT -01:00] America/Scoresbysund" offset="0" />
	<zone id="America/Sitka" name="[GMT -09:00] America/Sitka" offset="-28800000" />
	<zone id="America/St_Johns" name="[GMT -03:30] America/St Johns" offset="-9000000" />
	<zone id="America/St_Kitts" name="[GMT -04:00] America/St Kitts" offset="-14400000" />
	<zone id="America/St_Lucia" name="[GMT -04:00] America/St Lucia" offset="-14400000" />
	<zone id="America/St_Thomas" name="[GMT -04:00] America/St Thomas" offset="-14400000" />
	<zone id="America/St_Vincent" name="[GMT -04:00] America/St Vincent" offset="-14400000" />
	<zone id="America/Swift_Current" name="[GMT -06:00] America/Swift Current" offset="-21600000" />
	<zone id="America/Tegucigalpa" name="[GMT -06:00] America/Tegucigalpa" offset="-21600000" />
	<zone id="America/Thule" name="[GMT -04:00] America/Thule" offset="-10800000" />
	<zone id="America/Thunder_Bay" name="[GMT -05:00] America/Thunder Bay" offset="-14400000" />
	<zone id="America/Toronto" name="[GMT -05:00] America/Toronto" offset="-14400000" />
	<zone id="America/Tortola" name="[GMT -04:00] America/Tortola" offset="-14400000" />
	<zone id="America/Vancouver" name="[GMT -08:00] America/Vancouver" offset="-25200000" />
	<zone id="America/Whitehorse" name="[GMT -08:00] America/Whitehorse" offset="-25200000" />
	<zone id="America/Winnipeg" name="[GMT -06:00] America/Winnipeg" offset="-18000000" />
	<zone id="America/Yakutat" name="[GMT -09:00] America/Yakutat" offset="-28800000" />
	<zone id="America/Yellowknife" name="[GMT -07:00] America/Yellowknife" offset="-21600000" />
	<zone id="Antarctica/Casey" name="[GMT +08:00] Antarctica/Casey" offset="28800000" />
	<zone id="Antarctica/Davis" name="[GMT +07:00] Antarctica/Davis" offset="25200000" />
	<zone id="Antarctica/DumontDUrville" name="[GMT +10:00] Antarctica/DumontDUrville" offset="36000000" />
	<zone id="Antarctica/Macquarie" name="[GMT +11:00] Antarctica/Macquarie" offset="39600000" />
	<zone id="Antarctica/Mawson" name="[GMT +05:00] Antarctica/Mawson" offset="18000000" />
	<zone id="Antarctica/McMurdo" name="[GMT +12:00] Antarctica/McMurdo" offset="43200000" />
	<zone id="Antarctica/Palmer" name="[GMT -04:00] Antarctica/Palmer" offset="-14400000" />
	<zone id="Antarctica/Rothera" name="[GMT -03:00] Antarctica/Rothera" offset="-10800000" />
	<zone id="Antarctica/Syowa" name="[GMT +03:00] Antarctica/Syowa" offset="10800000" />
	<zone id="Antarctica/Vostok" name="[GMT +06:00] Antarctica/Vostok" offset="21600000" />
	<zone id="Europe/Oslo" name="[GMT +01:00] Europe/Oslo" offset="7200000" />
	<zone id="Asia/Aden" name="[GMT +03:00] Asia/Aden" offset="10800000" />
	<zone id="Asia/Almaty" name="[GMT +06:00] Asia/Almaty" offset="21600000" />
	<zone id="Asia/Amman" name="[GMT +02:00] Asia/Amman" offset="10800000" />
	<zone id="Asia/Anadyr" name="[GMT +12:00] Asia/Anadyr" offset="43200000" />
	<zone id="Asia/Aqtau" name="[GMT +05:00] Asia/Aqtau" offset="18000000" />
	<zone id="Asia/Aqtobe" name="[GMT +05:00] Asia/Aqtobe" offset="18000000" />
	<zone id="Asia/Ashgabat" name="[GMT +05:00] Asia/Ashgabat" offset="18000000" />
	<zone id="Asia/Baghdad" name="[GMT +03:00] Asia/Baghdad" offset="10800000" />
	<zone id="Asia/Bahrain" name="[GMT +03:00] Asia/Bahrain" offset="10800000" />
	<zone id="Asia/Baku" name="[GMT +04:00] Asia/Baku" offset="18000000" />
	<zone id="Asia/Bangkok" name="[GMT +07:00] Asia/Bangkok" offset="25200000" />
	<zone id="Asia/Beirut" name="[GMT +02:00] Asia/Beirut" offset="10800000" />
	<zone id="Asia/Bishkek" name="[GMT +06:00] Asia/Bishkek" offset="21600000" />
	<zone id="Asia/Brunei" name="[GMT +08:00] Asia/Brunei" offset="28800000" />
	<zone id="Asia/Kolkata" name="[GMT +05:30] Asia/Kolkata" offset="19800000" />
	<zone id="Asia/Choibalsan" name="[GMT +08:00] Asia/Choibalsan" offset="28800000" />
	<zone id="Asia/Chongqing" name="[GMT +08:00] Asia/Chongqing" offset="28800000" />
	<zone id="Asia/Colombo" name="[GMT +05:30] Asia/Colombo" offset="19800000" />
	<zone id="Asia/Dhaka" name="[GMT +06:00] Asia/Dhaka" offset="21600000" />
	<zone id="Asia/Damascus" name="[GMT +02:00] Asia/Damascus" offset="10800000" />
	<zone id="Asia/Dili" name="[GMT +09:00] Asia/Dili" offset="32400000" />
	<zone id="Asia/Dubai" name="[GMT +04:00] Asia/Dubai" offset="14400000" />
	<zone id="Asia/Dushanbe" name="[GMT +05:00] Asia/Dushanbe" offset="18000000" />
	<zone id="Asia/Gaza" name="[GMT +02:00] Asia/Gaza" offset="10800000" />
	<zone id="Asia/Harbin" name="[GMT +08:00] Asia/Harbin" offset="28800000" />
	<zone id="Asia/Hebron" name="[GMT +02:00] Asia/Hebron" offset="10800000" />
	<zone id="Asia/Ho_Chi_Minh" name="[GMT +07:00] Asia/Ho Chi Minh" offset="25200000" />
	<zone id="Asia/Hong_Kong" name="[GMT +08:00] Asia/Hong Kong" offset="28800000" />
	<zone id="Asia/Hovd" name="[GMT +07:00] Asia/Hovd" offset="25200000" />
	<zone id="Asia/Irkutsk" name="[GMT +09:00] Asia/Irkutsk" offset="32400000" />
	<zone id="Europe/Istanbul" name="[GMT +02:00] Europe/Istanbul" offset="10800000" />
	<zone id="Asia/Jakarta" name="[GMT +07:00] Asia/Jakarta" offset="25200000" />
	<zone id="Asia/Jayapura" name="[GMT +09:00] Asia/Jayapura" offset="32400000" />
	<zone id="Asia/Jerusalem" name="[GMT +02:00] Asia/Jerusalem" offset="10800000" />
	<zone id="Asia/Kabul" name="[GMT +04:30] Asia/Kabul" offset="16200000" />
	<zone id="Asia/Kamchatka" name="[GMT +12:00] Asia/Kamchatka" offset="43200000" />
	<zone id="Asia/Karachi" name="[GMT +05:00] Asia/Karachi" offset="18000000" />
	<zone id="Asia/Kashgar" name="[GMT +08:00] Asia/Kashgar" offset="28800000" />
	<zone id="Asia/Kathmandu" name="[GMT +05:45] Asia/Kathmandu" offset="20700000" />
	<zone id="Asia/Khandyga" name="[GMT +10:00] Asia/Khandyga" offset="36000000" />
	<zone id="Asia/Krasnoyarsk" name="[GMT +08:00] Asia/Krasnoyarsk" offset="28800000" />
	<zone id="Asia/Kuala_Lumpur" name="[GMT +08:00] Asia/Kuala Lumpur" offset="28800000" />
	<zone id="Asia/Kuching" name="[GMT +08:00] Asia/Kuching" offset="28800000" />
	<zone id="Asia/Kuwait" name="[GMT +03:00] Asia/Kuwait" offset="10800000" />
	<zone id="Asia/Macau" name="[GMT +08:00] Asia/Macau" offset="28800000" />
	<zone id="Asia/Magadan" name="[GMT +12:00] Asia/Magadan" offset="43200000" />
	<zone id="Asia/Makassar" name="[GMT +08:00] Asia/Makassar" offset="28800000" />
	<zone id="Asia/Manila" name="[GMT +08:00] Asia/Manila" offset="28800000" />
	<zone id="Asia/Muscat" name="[GMT +04:00] Asia/Muscat" offset="14400000" />
	<zone id="Asia/Nicosia" name="[GMT +02:00] Asia/Nicosia" offset="10800000" />
	<zone id="Asia/Novokuznetsk" name="[GMT +07:00] Asia/Novokuznetsk" offset="25200000" />
	<zone id="Asia/Novosibirsk" name="[GMT +07:00] Asia/Novosibirsk" offset="25200000" />
	<zone id="Asia/Omsk" name="[GMT +07:00] Asia/Omsk" offset="25200000" />
	<zone id="Asia/Oral" name="[GMT +05:00] Asia/Oral" offset="18000000" />
	<zone id="Asia/Phnom_Penh" name="[GMT +07:00] Asia/Phnom Penh" offset="25200000" />
	<zone id="Asia/Pontianak" name="[GMT +07:00] Asia/Pontianak" offset="25200000" />
	<zone id="Asia/Pyongyang" name="[GMT +09:00] Asia/Pyongyang" offset="32400000" />
	<zone id="Asia/Qatar" name="[GMT +03:00] Asia/Qatar" offset="10800000" />
	<zone id="Asia/Qyzylorda" name="[GMT +06:00] Asia/Qyzylorda" offset="21600000" />
	<zone id="Asia/Rangoon" name="[GMT +06:30] Asia/Rangoon" offset="23400000" />
	<zone id="Asia/Riyadh" name="[GMT +03:00] Asia/Riyadh" offset="10800000" />
	<zone id="Asia/Sakhalin" name="[GMT +11:00] Asia/Sakhalin" offset="39600000" />
	<zone id="Asia/Samarkand" name="[GMT +05:00] Asia/Samarkand" offset="18000000" />
	<zone id="Asia/Seoul" name="[GMT +09:00] Asia/Seoul" offset="32400000" />
	<zone id="Asia/Shanghai" name="[GMT +08:00] Asia/Shanghai" offset="28800000" />
	<zone id="Asia/Singapore" name="[GMT +08:00] Asia/Singapore" offset="28800000" />
	<zone id="Asia/Taipei" name="[GMT +08:00] Asia/Taipei" offset="28800000" />
	<zone id="Asia/Tashkent" name="[GMT +05:00] Asia/Tashkent" offset="18000000" />
	<zone id="Asia/Tbilisi" name="[GMT +04:00] Asia/Tbilisi" offset="14400000" />
	<zone id="Asia/Tehran" name="[GMT +03:30] Asia/Tehran" offset="16200000" />
	<zone id="Asia/Thimphu" name="[GMT +06:00] Asia/Thimphu" offset="21600000" />
	<zone id="Asia/Tokyo" name="[GMT +09:00] Asia/Tokyo" offset="32400000" />
	<zone id="Asia/Ulaanbaatar" name="[GMT +08:00] Asia/Ulaanbaatar" offset="28800000" />
	<zone id="Asia/Urumqi" name="[GMT +08:00] Asia/Urumqi" offset="28800000" />
	<zone id="Asia/Ust-Nera" name="[GMT +11:00] Asia/Ust-Nera" offset="39600000" />
	<zone id="Asia/Vientiane" name="[GMT +07:00] Asia/Vientiane" offset="25200000" />
	<zone id="Asia/Vladivostok" name="[GMT +11:00] Asia/Vladivostok" offset="39600000" />
	<zone id="Asia/Yakutsk" name="[GMT +10:00] Asia/Yakutsk" offset="36000000" />
	<zone id="Asia/Yekaterinburg" name="[GMT +06:00] Asia/Yekaterinburg" offset="21600000" />
	<zone id="Asia/Yerevan" name="[GMT +04:00] Asia/Yerevan" offset="14400000" />
	<zone id="Atlantic/Azores" name="[GMT -01:00] Atlantic/Azores" offset="0" />
	<zone id="Atlantic/Bermuda" name="[GMT -04:00] Atlantic/Bermuda" offset="-10800000" />
	<zone id="Atlantic/Canary" name="[GMT +00:00] Atlantic/Canary" offset="3600000" />
	<zone id="Atlantic/Cape_Verde" name="[GMT -01:00] Atlantic/Cape Verde" offset="-3600000" />
	<zone id="Atlantic/Faroe" name="[GMT +00:00] Atlantic/Faroe" offset="3600000" />
	<zone id="Atlantic/Madeira" name="[GMT +00:00] Atlantic/Madeira" offset="3600000" />
	<zone id="Atlantic/Reykjavik" name="[GMT +00:00] Atlantic/Reykjavik" offset="0" />
	<zone id="Atlantic/South_Georgia" name="[GMT -02:00] Atlantic/South Georgia" offset="-7200000" />
	<zone id="Atlantic/St_Helena" name="[GMT +00:00] Atlantic/St Helena" offset="0" />
	<zone id="Atlantic/Stanley" name="[GMT -03:00] Atlantic/Stanley" offset="-10800000" />
	<zone id="Australia/Sydney" name="[GMT +10:00] Australia/Sydney" offset="36000000" />
	<zone id="Australia/Adelaide" name="[GMT +09:30] Australia/Adelaide" offset="34200000" />
	<zone id="Australia/Brisbane" name="[GMT +10:00] Australia/Brisbane" offset="36000000" />
	<zone id="Australia/Broken_Hill" name="[GMT +09:30] Australia/Broken Hill" offset="34200000" />
	<zone id="Australia/Currie" name="[GMT +10:00] Australia/Currie" offset="36000000" />
	<zone id="Australia/Darwin" name="[GMT +09:30] Australia/Darwin" offset="34200000" />
	<zone id="Australia/Eucla" name="[GMT +08:45] Australia/Eucla" offset="31500000" />
	<zone id="Australia/Hobart" name="[GMT +10:00] Australia/Hobart" offset="36000000" />
	<zone id="Australia/Lord_Howe" name="[GMT +10:30] Australia/Lord Howe" offset="37800000" />
	<zone id="Australia/Lindeman" name="[GMT +10:00] Australia/Lindeman" offset="36000000" />
	<zone id="Australia/Melbourne" name="[GMT +10:00] Australia/Melbourne" offset="36000000" />
	<zone id="Australia/Perth" name="[GMT +08:00] Australia/Perth" offset="28800000" />
	<zone id="CET" name="[GMT +01:00] CET" offset="7200000" />
	<zone id="CST6CDT" name="[GMT -06:00] CST6CDT" offset="-18000000" />
	<zone id="Pacific/Easter" name="[GMT -06:00] Pacific/Easter" offset="-21600000" />
	<zone id="EET" name="[GMT +02:00] EET" offset="10800000" />
	<zone id="EST" name="[GMT -05:00] EST" offset="-18000000" />
	<zone id="EST5EDT" name="[GMT -05:00] EST5EDT" offset="-14400000" />
	<zone id="Europe/Dublin" name="[GMT +00:00] Europe/Dublin" offset="3600000" />
	<zone id="Europe/Amsterdam" name="[GMT +01:00] Europe/Amsterdam" offset="7200000" />
	<zone id="Europe/Andorra" name="[GMT +01:00] Europe/Andorra" offset="7200000" />
	<zone id="Europe/Athens" name="[GMT +02:00] Europe/Athens" offset="10800000" />
	<zone id="Europe/London" name="[GMT +00:00] Europe/London" offset="3600000" />
	<zone id="Europe/Belgrade" name="[GMT +01:00] Europe/Belgrade" offset="7200000" />
	<zone id="Europe/Berlin" name="[GMT +01:00] Europe/Berlin" offset="7200000" />
	<zone id="Europe/Prague" name="[GMT +01:00] Europe/Prague" offset="7200000" />
	<zone id="Europe/Brussels" name="[GMT +01:00] Europe/Brussels" offset="7200000" />
	<zone id="Europe/Bucharest" name="[GMT +02:00] Europe/Bucharest" offset="10800000" />
	<zone id="Europe/Budapest" name="[GMT +01:00] Europe/Budapest" offset="7200000" />
	<zone id="Europe/Zurich" name="[GMT +01:00] Europe/Zurich" offset="7200000" />
	<zone id="Europe/Chisinau" name="[GMT +02:00] Europe/Chisinau" offset="10800000" />
	<zone id="Europe/Copenhagen" name="[GMT +01:00] Europe/Copenhagen" offset="7200000" />
	<zone id="Europe/Gibraltar" name="[GMT +01:00] Europe/Gibraltar" offset="7200000" />
	<zone id="Europe/Helsinki" name="[GMT +02:00] Europe/Helsinki" offset="10800000" />
	<zone id="Europe/Kaliningrad" name="[GMT +03:00] Europe/Kaliningrad" offset="10800000" />
	<zone id="Europe/Kiev" name="[GMT +02:00] Europe/Kiev" offset="10800000" />
	<zone id="Europe/Lisbon" name="[GMT +00:00] Europe/Lisbon" offset="3600000" />
	<zone id="Europe/Luxembourg" name="[GMT +01:00] Europe/Luxembourg" offset="7200000" />
	<zone id="Europe/Madrid" name="[GMT +01:00] Europe/Madrid" offset="7200000" />
	<zone id="Europe/Malta" name="[GMT +01:00] Europe/Malta" offset="7200000" />
	<zone id="Europe/Minsk" name="[GMT +03:00] Europe/Minsk" offset="10800000" />
	<zone id="Europe/Monaco" name="[GMT +01:00] Europe/Monaco" offset="7200000" />
	<zone id="Europe/Moscow" name="[GMT +04:00] Europe/Moscow" offset="14400000" />
	<zone id="Europe/Paris" name="[GMT +01:00] Europe/Paris" offset="7200000" />
	<zone id="Europe/Riga" name="[GMT +02:00] Europe/Riga" offset="10800000" />
	<zone id="Europe/Rome" name="[GMT +01:00] Europe/Rome" offset="7200000" />
	<zone id="Europe/Samara" name="[GMT +04:00] Europe/Samara" offset="14400000" />
	<zone id="Europe/Simferopol" name="[GMT +02:00] Europe/Simferopol" offset="10800000" />
	<zone id="Europe/Sofia" name="[GMT +02:00] Europe/Sofia" offset="10800000" />
	<zone id="Europe/Stockholm" name="[GMT +01:00] Europe/Stockholm" offset="7200000" />
	<zone id="Europe/Tallinn" name="[GMT +02:00] Europe/Tallinn" offset="10800000" />
	<zone id="Europe/Tirane" name="[GMT +01:00] Europe/Tirane" offset="7200000" />
	<zone id="Europe/Uzhgorod" name="[GMT +02:00] Europe/Uzhgorod" offset="10800000" />
	<zone id="Europe/Vaduz" name="[GMT +01:00] Europe/Vaduz" offset="7200000" />
	<zone id="Europe/Vienna" name="[GMT +01:00] Europe/Vienna" offset="7200000" />
	<zone id="Europe/Vilnius" name="[GMT +02:00] Europe/Vilnius" offset="10800000" />
	<zone id="Europe/Volgograd" name="[GMT +04:00] Europe/Volgograd" offset="14400000" />
	<zone id="Europe/Warsaw" name="[GMT +01:00] Europe/Warsaw" offset="7200000" />
	<zone id="Europe/Zaporozhye" name="[GMT +02:00] Europe/Zaporozhye" offset="10800000" />
	<zone id="Etc/GMT" name="[GMT +00:00] Etc/GMT" offset="0" />
	<zone id="HST" name="[GMT -10:00] HST" offset="-36000000" />
	<zone id="Indian/Antananarivo" name="[GMT +03:00] Indian/Antananarivo" offset="10800000" />
	<zone id="Indian/Chagos" name="[GMT +06:00] Indian/Chagos" offset="21600000" />
	<zone id="Indian/Christmas" name="[GMT +07:00] Indian/Christmas" offset="25200000" />
	<zone id="Indian/Cocos" name="[GMT +06:30] Indian/Cocos" offset="23400000" />
	<zone id="Indian/Comoro" name="[GMT +03:00] Indian/Comoro" offset="10800000" />
	<zone id="Indian/Kerguelen" name="[GMT +05:00] Indian/Kerguelen" offset="18000000" />
	<zone id="Indian/Mahe" name="[GMT +04:00] Indian/Mahe" offset="14400000" />
	<zone id="Indian/Maldives" name="[GMT +05:00] Indian/Maldives" offset="18000000" />
	<zone id="Indian/Mauritius" name="[GMT +04:00] Indian/Mauritius" offset="14400000" />
	<zone id="Indian/Mayotte" name="[GMT +03:00] Indian/Mayotte" offset="10800000" />
	<zone id="Indian/Reunion" name="[GMT +04:00] Indian/Reunion" offset="14400000" />
	<zone id="Pacific/Kwajalein" name="[GMT +12:00] Pacific/Kwajalein" offset="43200000" />
	<zone id="MET" name="[GMT +01:00] MET" offset="7200000" />
	<zone id="MST" name="[GMT -07:00] MST" offset="-25200000" />
	<zone id="MST7MDT" name="[GMT -07:00] MST7MDT" offset="-21600000" />
	<zone id="Pacific/Auckland" name="[GMT +12:00] Pacific/Auckland" offset="43200000" />
	<zone id="Pacific/Chatham" name="[GMT +12:45] Pacific/Chatham" offset="45900000" />
	<zone id="PST8PDT" name="[GMT -08:00] PST8PDT" offset="-25200000" />
	<zone id="Pacific/Apia" name="[GMT +13:00] Pacific/Apia" offset="46800000" />
	<zone id="Pacific/Chuuk" name="[GMT +10:00] Pacific/Chuuk" offset="36000000" />
	<zone id="Pacific/Efate" name="[GMT +11:00] Pacific/Efate" offset="39600000" />
	<zone id="Pacific/Enderbury" name="[GMT +13:00] Pacific/Enderbury" offset="46800000" />
	<zone id="Pacific/Fakaofo" name="[GMT +13:00] Pacific/Fakaofo" offset="46800000" />
	<zone id="Pacific/Fiji" name="[GMT +12:00] Pacific/Fiji" offset="43200000" />
	<zone id="Pacific/Funafuti" name="[GMT +12:00] Pacific/Funafuti" offset="43200000" />
	<zone id="Pacific/Galapagos" name="[GMT -06:00] Pacific/Galapagos" offset="-21600000" />
	<zone id="Pacific/Gambier" name="[GMT -09:00] Pacific/Gambier" offset="-32400000" />
	<zone id="Pacific/Guadalcanal" name="[GMT +11:00] Pacific/Guadalcanal" offset="39600000" />
	<zone id="Pacific/Guam" name="[GMT +10:00] Pacific/Guam" offset="36000000" />
	<zone id="Pacific/Honolulu" name="[GMT -10:00] Pacific/Honolulu" offset="-36000000" />
	<zone id="Pacific/Johnston" name="[GMT -10:00] Pacific/Johnston" offset="-36000000" />
	<zone id="Pacific/Kiritimati" name="[GMT +14:00] Pacific/Kiritimati" offset="50400000" />
	<zone id="Pacific/Kosrae" name="[GMT +11:00] Pacific/Kosrae" offset="39600000" />
	<zone id="Pacific/Majuro" name="[GMT +12:00] Pacific/Majuro" offset="43200000" />
	<zone id="Pacific/Marquesas" name="[GMT -09:30] Pacific/Marquesas" offset="-34200000" />
	<zone id="Pacific/Midway" name="[GMT -11:00] Pacific/Midway" offset="-39600000" />
	<zone id="Pacific/Nauru" name="[GMT +12:00] Pacific/Nauru" offset="43200000" />
	<zone id="Pacific/Niue" name="[GMT -11:00] Pacific/Niue" offset="-39600000" />
	<zone id="Pacific/Norfolk" name="[GMT +11:30] Pacific/Norfolk" offset="41400000" />
	<zone id="Pacific/Noumea" name="[GMT +11:00] Pacific/Noumea" offset="39600000" />
	<zone id="Pacific/Pago_Pago" name="[GMT -11:00] Pacific/Pago Pago" offset="-39600000" />
	<zone id="Pacific/Palau" name="[GMT +09:00] Pacific/Palau" offset="32400000" />
	<zone id="Pacific/Pitcairn" name="[GMT -08:00] Pacific/Pitcairn" offset="-28800000" />
	<zone id="Pacific/Pohnpei" name="[GMT +11:00] Pacific/Pohnpei" offset="39600000" />
	<zone id="Pacific/Port_Moresby" name="[GMT +10:00] Pacific/Port Moresby" offset="36000000" />
	<zone id="Pacific/Rarotonga" name="[GMT -10:00] Pacific/Rarotonga" offset="-36000000" />
	<zone id="Pacific/Saipan" name="[GMT +10:00] Pacific/Saipan" offset="36000000" />
	<zone id="Pacific/Tahiti" name="[GMT -10:00] Pacific/Tahiti" offset="-36000000" />
	<zone id="Pacific/Tarawa" name="[GMT +12:00] Pacific/Tarawa" offset="43200000" />
	<zone id="Pacific/Tongatapu" name="[GMT +13:00] Pacific/Tongatapu" offset="46800000" />
	<zone id="Pacific/Wake" name="[GMT +12:00] Pacific/Wake" offset="43200000" />
	<zone id="Pacific/Wallis" name="[GMT +12:00] Pacific/Wallis" offset="43200000" />
	<zone id="Etc/UCT" name="[GMT +00:00] Etc/UCT" offset="0" />
	<zone id="UTC" name="[GMT +00:00] UTC" offset="0" />
	<zone id="Etc/UTC" name="[GMT +00:00] Etc/UTC" offset="0" />
	<zone id="WET" name="[GMT +00:00] WET" offset="3600000" />'''

tzlist=re.findall('<zone id="(.*)" name',ruby)
for tz in tzlist:
	zone = pytz.timezone(tz)
	print zone # zone id name
	localnow = datetime.datetime.now(zone) # zone local time
	print localnow
	tzFormat = '%Y%m%dT%H%M%S' # 20140731T140113
	print localnow.strftime(tzFormat)
	
	
	# --------------------------------
	# date time to time stamp
	timestamp = time.mktime(localnow.timetuple())
	print timestamp
	
	# time stamp to date time
	# find the timestamp from original 'msgheaderlist' response
	timeTuple=time.localtime(1406856796.000)
	print timeTuple
	
	# date time to time stamp
	timestamp = time.mktime(timeTuple)
	print timestamp
	print '~~~'
	
	
	
	
		
		
		