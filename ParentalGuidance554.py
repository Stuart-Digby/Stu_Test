#!/usr/bin/env python

import requests
import os
from time import gmtime, time, strftime, asctime
from urllib import urlopen
import xml.etree.ElementTree as ET
import datetime

do_ingest = True

services = {
    #'http://youview.com/test/IP/youviewip12':[]
    # 'http://youview.com/test/IP/youviewip17':[],
    'http://youview.com/test/IP/SUB_SD_bADmix':[]
}

sid_ep = 'http://youview.co.uk/Youview_SERVICE'
expiration = '2015-02-04T23:59:58Z'

ingest_url = 'https://ingest-int01.ccosvc.com/ingest/transaction/'
credentials = ('canvas', 'canvas')

if not os.path.exists('xml'):
    os.makedirs('xml')

logf = open('exp.log', 'a')


def ingest(fname):
    f = open(fname, 'r')
    xml_data = f.read()
    f.close()
    resp = requests.post(ingest_url, data=xml_data, auth=credentials)
    print resp
    return resp.status_code, resp.headers['location']


def write_xml(root, fname):
    tree = ET.ElementTree(root)
    f = open(fname, 'w')
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    tree.write(f)
    f.close()


def t_to_str(time):
    return strftime("%Y-%m-%dT%H:%M:%SZ", gmtime(time))

series_names = [
    'East Enders',
    'Top Gear',
    'Coronation Street'
]

curtime = time()
curtime = curtime - curtime % (24*60*60)
midnight = curtime
eight_am = midnight + (8 * 60 * 60)

RatingsList = ["15", "Unrated", "Delete", "Unrated", "15", "15", "Delete",
               "Unrated", "G", "Unrated"]  ## This sets the order of ratings & deleted events
dailyRatings = ["Unrated", "G", "15"]
RatingArray = {
    'Unrated': 'http://bbfc.org.uk/BBFCRatingCS/2002#U',
    'U': 'http://bbfc.org.uk/BBFCRatingCS/2002#U',
    '15': 'http://bbfc.org.uk/BBFCRatingCS/2002#15',
    'G': 'urn:dtg:metadata:cs:DTGContentWarningCS:2011:G',
    # 'http://bbc.co.uk/refdata/mpeg7cs/DentonContentWarningCS/2010/04/19#G', #'urn:dtg:metadata:cs:DTGContentWarningCS:2011:G',
    'Delete': ''}

for i in range(0, 120):  # 120 = 10 hours of events (i.e. 8am - 6pm)
    ######## CANTST-10459 ########################
    ### This bit works out what character to insert at the start of the event title string    
    j = i % len(RatingsList) 

    ######## CANTST-10459 ########################
    event = {
    'id':'123123' + str(i),
    'title':str(RatingsList[j]) + " " + series_names[(i / 10) % 3] + ' ' + str(i % 10 + 1),  ### The 10's here must match the number ov items in RatingsList
    'scheduleSlot':t_to_str(eight_am + i*5*60),
    'time':eight_am + i*5*60,
    'duration':'300',
    'i':i,
    'ratingString':str(RatingArray[str(RatingsList[j])]),
    }
    ######## CANTST-10459 ########################
    ### Ignores every 4th event and simply does not add it to the services list
    if RatingsList[j] != "Delete":
        services['http://youview.com/test/IP/SUB_SD_bADmix'].append(event)
    ######## CANTST-10459 ########################

################ Events to transition watershed boundries #########
day_of_the_week = datetime.date.today().isoweekday()
k = day_of_the_week % len(dailyRatings)

evening_event = {
    'id':'123123' + str(i + 1),
    'title':str(dailyRatings[k]) + " Evening Event",
    'scheduleSlot':t_to_str(eight_am + (i + 1)*5*60),
    'time':midnight,
    'duration': str(6 * 60 * 60),
    'i': (i + 1),
    'ratingString':str(RatingArray[str(dailyRatings[k])]),
    }
services[''].append(evening_event)

morning_event = {
    'id':'123123' + str(i + 2),
    'title':str(dailyRatings[k]) + " Morning Event",
    'scheduleSlot':t_to_str(midnight),
    'time':midnight,
    'duration': str(8 * 60 * 60),
    'i': (i + 2),
    'ratingString':str(RatingArray[str(dailyRatings[k])]),
    }
services['http://youview.com/test/IP/SUB_SD_bADmix'].append(morning_event)
################ Events to transition watershed boundries #########


for full_name in sorted(services.keys()):
    sname = full_name.split('/')[-1]
    events = services[full_name]

    schedule_root = ET.Element('TVAMain')
    schedule_root.attrib = {'xml:lang':'en-GB', 'xmlns':'urn:tva:metadata:2010', 'xmlns:tva2':'urn:tva:metadata:extended:2010', 'xmlns:mpeg7':'urn:tva:mpeg7:2008', 'xmlns:yv':'http://refdata.youview.com/schemas/Metadata/2012-11-19', 'xmlns:xsi':'http://www.w3.org/2001/XMLSchema-instance', 'xsi:schemaLocation':'http://refdata.youview.com/schemas/Metadata/2012-10-16 ../schemas/youview_metadata_2012-10-16.xsd'}
    pd = ET.SubElement(schedule_root, 'ProgramDescription')
    pt = ET.SubElement(pd, 'ProgramLocationTable')
    sch = ET.SubElement(pt, 'Schedule')
    sch.attrib = {'xml:lang':'en', 'serviceIDRef':full_name, 'start':'2011-12-01T23:35:00Z', 'end':'2024-12-01T23:35:00Z'}

    ep_ev_root = ET.Element('TVAMain')
    ep_ev_root.attrib = {'xmlns:xsi':'http://www.w3.org/2001/XMLSchema-instance', 'xmlns:tva2':'urn:tva:metadata:extended:2010', 'xmlns:yv':'http://refdata.youview.com/schemas/2011-02-18', 'xmlns':'urn:tva:metadata:2010', 'xmlns:mpeg7':'urn:tva:mpeg7:2008', 'xmlns:tva':'urn:tva:metadata:2010', 'xml:lang':'en-GB', 'xsi:schemaLocation':'http://refdata.youview.com/schemas/Metadata/2012-11-19 ../schemas/youview_metadata_2012-11-19.xsd'}
    pd = ET.SubElement(ep_ev_root, 'ProgramDescription')
    pit = ET.SubElement(pd, 'ProgramInformationTable')
    git = ET.SubElement(pd, 'GroupInformationTable')

    count = 0
    
    for event in events:
        count += 1
        crid = 'crid://youview.com/EV-' + str(event['id'] + sname)
        gi_crid = crid.replace('EV', 'EP')

        # generate ScheduleEvent
        ev = ET.SubElement(sch, 'ScheduleEvent')
        ev.attrib = {'xsi:type':'yv:ExtendedScheduleEventType'}
        p = ET.SubElement(ev, 'Program')
        p.attrib = {'crid':crid}
        purl = ET.SubElement(ev, 'ProgramURL')
        purl.text = 'tag:talktalk.co.uk,2012-05-27:event:disney_channel:uk:' + event['id'] + sname
        imi = ET.SubElement(ev, 'InstanceMetadataId')
        imi.text = 'imi:youview.com/' + event['id'] + sname
        ind = ET.SubElement(ev, 'InstanceDescription')
        t = ET.SubElement(ind, 'Title')
        t.text = event['title'] + ' IP'
        s = ET.SubElement(ind, 'Synopsis')
        s.attrib = {'length':'medium'}
        s.text = 'Medium length synopsis for ' + event['title'] + '.'
        g = ET.SubElement(ind, 'Genre')
        g.attrib = {'type':'secondary', 'href':'urn:dtg:metadata:cs:DTGGenreCS:2010-11:0'}
        g = ET.SubElement(ind, 'Genre')
        g.attrib = {'type':'other', 'href':'http://refdata.youview.com/mpeg7cs/YouViewPublicationTypeCS/2012-09-06#broadcast-dummy'}
        aa = ET.SubElement(ind, 'AVAttributes')
        oi = ET.SubElement(ind, 'OtherIdentifier')
        oi.attrib = {'authority':'pcrid.dmol.co.uk'}
        oi.text = 'crid://dmol.co.uk/100' + str(int(event['i'])) + sname
        oi = ET.SubElement(ind, 'OtherIdentifier')
        oi.attrib = {'authority':'scrid.dmol.co.uk'}
        oi.text = 'crid://dmol.co.uk/101' + str(int(event['i'] / 4)) + sname

        pst = ET.SubElement(ev, 'PublishedStartTime')
        pst.text = event['scheduleSlot']
        pd = ET.SubElement(ev, 'PublishedDuration')
        pd.text = 'PT' + str(int(event['duration'])/60/60) + 'H' + str(int(event['duration'])/60%60).zfill(2) + 'M'
        fr = ET.SubElement(ev, 'Free')
        fr.attrib = {'value':'true'}
        ast = ET.SubElement(ev, 'yv:ActualStartTime')
        ast.text = event['scheduleSlot']
        ad = ET.SubElement(ev, 'yv:ActualDuration')
        ad.text = 'PT' + str(int(event['duration'])/60/60) + 'H' + str(int(event['duration'])/60%60).zfill(2) + 'M'

        # generate ProgramInformation
        #expiration = '2015-02-04T23:59:58Z'
        pi = ET.SubElement(pit, 'ProgramInformation')
        pi.attrib = {'xml:lang':'eng', 'programId':crid, 'fragmentExpirationDate':expiration}
        bd = ET.SubElement(pi, 'BasicDescription')
        bd.attrib = {'xsi:type':'tva2:ExtendedContentDescriptionType'}
        t = ET.SubElement(bd, 'Title')
        t.attrib = {'type':'main'}
        t.text = event['title'] + ' IP'
        st = ET.SubElement(bd, 'ShortTitle')
        st.attrib = {'length':'10'}
        st.text = 'shorttitle'
        sn = ET.SubElement(bd, 'Synopsis')
        sn.attrib = {'length':'short'}
        sn.text = event['title'] + ' short synopsis.'
        sn = ET.SubElement(bd, 'Synopsis')
        sn.attrib = {'length':'medium'}
        sn.text = event['title'] + ' medium synopsis.'
        sn = ET.SubElement(bd, 'Synopsis')
        sn.attrib = {'length':'long'}
        sn.text = event['title'] + ' long synopsis.'
        
        if event['ratingString'] != '':
            pg = ET.SubElement(bd, 'ParentalGuidance')
            pr = ET.SubElement(pg, 'mpeg7:ParentalRating')
            et = ET.SubElement(pg, 'ExplanatoryText')
            et.attrib = {'length':'long'}
            et.text = 'Explanatory text'
            pr.attrib = {'href':event['ratingString']}
            #print "########", event['ratingString']
        #pr.attrib = {'href':RatingArray[str(k)]}
##        elif event['i'] % 4 == 2:
##            pr.attrib = {'href':'http://bbfc.org.uk/BBFCRatingCS/2002#U'}
##        elif event['i'] % 4 == 3:
##            pr.attrib = {'href':'http://bbfc.org.uk/BBFCRatingCS/2002#U'}
##        elif event['i'] % 8 == 1:
##            pr.attrib = {'href':'http://bbfc.org.uk/BBFCRatingCS/2002#U'}
##        elif event['i'] % 8 == 5:
##            pr.attrib = {'href':'http://bbfc.org.uk/BBFCRatingCS/2002#15'}
##        else:
##            pr.attrib = {'href':'http://bbfc.org.uk/BBFCRatingCS/2002#U'}
        ln = ET.SubElement(bd, 'Language')
        ln.attrib = {'type':'original'}
        ln.text = 'eng'
        rm = ET.SubElement(bd, 'RelatedMaterial')
        rm.attrib = {'xsi:type':'tva2:ExtendedRelatedMaterialType'}
        rmh = ET.SubElement(rm, 'HowRelated')
        rmh.attrib = {'href':'urn:tva:metadata:cs:HowRelatedCS:2010:19'}
        rmf = ET.SubElement(rm, 'Format')
        rmf.attrib = {'href':'urn:mpeg:mpeg7:cs:FileFormatCS:2001:1'}
        rmfml = ET.SubElement(rm, 'MediaLocator')
        rmfmu = ET.SubElement(rmfml, 'mpeg7:MediaUri')
        rmfmu.text = 'http://images.ccosvc.com/YouviewImages/Data_image_templates/ev_template.png'
        rmfpt = ET.SubElement(rm, 'PromotionalText')
        rmfpt.text = 'This is an jpeg image format'
        rmfcp = ET.SubElement(rm, 'tva2:ContentProperties')
        rmfcpa = ET.SubElement(rmfcp, 'tva2:ContentAttributes')
        rmfcpa.attrib = {'xsi:type':'tva2:StillImageContentAttributesType'}
        rmfcpaw = ET.SubElement(rmfcpa, 'tva2:Width')
        rmfcpaw.text = '640'
        rmfcpah = ET.SubElement(rmfcpa, 'tva2:Height')
        rmfcpah.text = '360'
        rmfcpai = ET.SubElement(rmfcpa, 'tva2:IntendedUse')
        rmfcpai.attrib = {'href':'http://refdata.youview.com/mpeg7cs/YouViewImageUsageCS/2010-09-23#role-primary'}

        pd = ET.SubElement(bd, 'ProductionDate')
        tp = ET.SubElement(pd, 'TimePoint')
        tp.text = '2011-10-28'
        d = ET.SubElement(bd, 'Duration')
        d.text = 'PT' + str(int(event['duration'])/60/60) + 'H' + str(int(event['duration'])/60%60).zfill(2) + 'M' + str(int(event['duration'])%60).zfill(2) + 'S'
        oi = ET.SubElement(pi, 'OtherIdentifier')
        oi.attrib = {'authority':'version.youview.com'}
        oi.text = crid
        df = ET.SubElement(pi, 'DerivedFrom')
        # Same as GroupInformation crid
        df.attrib = {'crid':gi_crid}

        # generate GroupInformation
        gi = ET.SubElement(git, 'GroupInformation')
        gi.attrib = {'xml:lang':'eng', 'groupId':gi_crid, 'ordered':'true', 'fragmentExpirationDate':expiration, 'serviceIDRef':sid_ep}
        gt = ET.SubElement(gi, 'GroupType')
        gt.attrib = {'xsi:type':'ProgramGroupTypeType', 'value':'programConcept'}
        bd = ET.SubElement(gi, 'BasicDescription')
        t = ET.SubElement(bd, 'Title')
        t.attrib = {'type':'main'}
        t.text = event['title'] + ' IP'
        st = ET.SubElement(bd, 'ShortTitle')
        st.attrib = {'length':'10'}
        st.text = 'shorttitle'
        sn = ET.SubElement(bd, 'Synopsis')
        sn.attrib = {'length':'short'}
        sn.text = event['title'] + ' with short synopsis'
        sn = ET.SubElement(bd, 'Synopsis')
        sn.attrib = {'length':'medium'}
        sn.text = event['title'] + ' with medium synopsis'
        sn = ET.SubElement(bd, 'Synopsis')
        sn.attrib = {'length':'long'}
        sn.text = event['title'] + ' with long synopsis'
        g = ET.SubElement(bd, 'Genre')
        g.attrib = {'type':'main', 'href':'urn:tva:metadata:cs:MediaTypeCS:2005:7.1.3'}
        g = ET.SubElement(bd, 'Genre')
        g.attrib = {'type':'main', 'href':'urn:tva:metadata:cs:ContentCS:2010:3.5.7'}
        g = ET.SubElement(bd, 'Genre')
        g.attrib = {'type':'main', 'href':'urn:tva:metadata:cs:OriginationCS:2005:5.8'}
        oi = ET.SubElement(gi, 'OtherIdentifier')
        oi.attrib = {'authority':'episodes.youview.com'}
        oi.text = gi_crid

    prefix = strftime("%Y_%m_%d_%H_%M_%S", gmtime(midnight))
    schedule = 'xml/' + prefix + '_schedule_' + sname + '.xml'
    ep_ev = 'xml/' + prefix + '_ep_ev_' + sname + '.xml'

    write_xml(schedule_root, schedule)
    write_xml(ep_ev_root, ep_ev)

    logf.write(asctime() + ' ' + sname + ' ' + str(count) + '\n')

    if do_ingest:
        #status, location = ingest(ep_ev)
        print ep_ev
        status, location = ingest(ep_ev)
        if status != 202:
            logf.write('  could not ingest ' + ep_ev + ' status:' + str(status) + '\n')
        else:
            logf.write('  ingested ' + ep_ev + ' location:' + location + '\n')
		
        status, location = ingest(schedule)
        if status != 202:
            logf.write('  could not ingest ' + schedule + ' status:' + str(status) + '\n')
        else:
            logf.write('  ingested ' + schedule + ' location: ' + location + '\n')

logf.close()