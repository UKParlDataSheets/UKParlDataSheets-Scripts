<?php

require_once 'funcs.php';

$dom = new DOMDocument();
$dom->loadXML(file_get_contents('Commons.xml'));

$outFile = fopen('commonsV1.csv', 'w');

$headings = array(
    'Member_Id',
    'Dods_Id',
    'Pims_Id',
    'DisplayAs',
    'ListAs',
    'FullTitle',
    'LayingMinisterName',
    'DateOfBirth',
    'DateOfDeath',
    'Gender',
    'Party',
    'House',
    'MemberFrom',
    'HouseStartDate',
    'HouseEndDate',
    'CurrentStatus_Id',
    'CurrentStatus_IsActive',
    'CurrentStatus_Name',
    'CurrentStatus_Reason',
    'CurrentStatus_StartDate',
);

for ($i = 1; $i <= 4; $i++) {
    $headings = array_merge( $headings, array(
        'Address' . $i . '_Type_Id',
        'Address' . $i . '_Type',
        'Address' . $i . '_IsPreferred',
        'Address' . $i . '_IsPhysical',
        'Address' . $i . '_Note',
        'Address' . $i . '_Address1',
        'Address' . $i . '_Address2',
        'Address' . $i . '_Address3',
        'Address' . $i . '_Address4',
        'Address' . $i . '_Address5',
        'Address' . $i . '_Postcode',
        'Address' . $i . '_Phone',
        'Address' . $i . '_Fax',
        'Address' . $i . '_Email',
    ) );
}

fputcsv($outFile, $headings);

foreach($dom->getElementsByTagName('Member') as $domElement) {

    $data = array(
        $domElement->getAttribute('Member_Id'),
        $domElement->getAttribute('Dods_Id'),
        $domElement->getAttribute('Pims_Id'),
    );


    foreach(array('DisplayAs','ListAs','FullTitle','LayingMinisterName','DateOfBirth','DateOfDeath','Gender','Party','House','MemberFrom','HouseStartDate','HouseEndDate') as $field) {
        $elements = $domElement->getElementsByTagName($field);
        $data[] = $elements->length > 0 ? DOMinnerText($elements->item(0)) : '';
    }

    $currentStatusElements = $domElement->getElementsByTagName('CurrentStatus');
    if ($currentStatusElements->length > 0) {
        $currentStatusElement = $currentStatusElements->item(0);

        $data[] = $currentStatusElement->getAttribute('Id');
        $data[] = $currentStatusElement->getAttribute('IsActive');

        foreach(array('Name','Reason','StartDate') as $field) {
            $elements = $currentStatusElement->getElementsByTagName($field);
            $data[] = $elements->length > 0 ? DOMinnerText($elements->item(0)) : '';
        }
    } else {
        $data[] = '';
        $data[] = '';
        $data[] = '';
        $data[] = '';
        $data[] = '';
    }

    $addressElements = $domElement->getElementsByTagName('Address');
    for ($i = 0; $i <= 3; $i++) {
        if ( $addressElements->length > $i ) {
            $addressElement = $addressElements->item( $i );

            $data[] = $addressElement->getAttribute( 'Type_Id' );

            foreach ( array( 'Type', 'IsPreferred','IsPhysical','Note','Address1','Address2','Address3','Address4','Address5','Postcode','Phone','Fax','Email' ) as $field ) {
                $elements = $addressElement->getElementsByTagName( $field );
                $data[]   = $elements->length > 0 ? DOMinnerText( $elements->item( 0 ) ) : '';
            }
        } else {
            // TODO need to do $data[] = ''; a bit, but seeing as nothing after, I don't care for now.
        }
    }
    
    fputcsv($outFile, $data);


}

