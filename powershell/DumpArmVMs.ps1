# this dumps all the vms from your subs
param(
    [Parameter(Position=1)]
    [string]$Subscription="",
    [Parameter(Position=2)]
    [string]$file="Azure-ARM-VMs.csv",
    [Parameter(Position=3)]
    [string]$SkipStatus=""
) 

<#
.SYNOPSIS
  Login to Azure if you are not currently logged in
#>

try
 {
     Get-AzSubscription | out-null
 }
 catch
 {
  if ($me -eq $null)
  {
      $me = Get-Credential
  } 
    Login-AzAccount -Credential $me
 }

# if they did not pass a subscription then just all of them minus the bogus ones
if ($Subscription -eq "")
{
    $subs = Get-AzSubscription | Where-Object Name -notin "Free Trial","Azure pass - Sponsorship","Access to Azure Active Directory","pay-as-you-go","microsoft Azure Enterprise","visual studio professional" | Where-object state -eq Enabled | Sort Name
}
else 
{
    $subs =  Get-AzSubscription -SubscriptionName $Subscription
}

$vmobjs = @()

foreach ($sub in $subs)
{
    
    Write-Host Processing subscription $sub.Name

    try
    {
        Select-AzSubscription -SubscriptionName $sub.Name -ErrorAction Continue

        $vms = Get-AzVm 

        foreach ($vm in $vms)
        {
            $vmInfo = [pscustomobject]@{
                'Subscription'=$sub.Name
                'Name'=$vm.Name
                'ResourceGroupName' = $vm.ResourceGroupName
                'Location' = $vm.Location
                'VMSize' = $vm.HardwareProfile.VMSize
                'DiskCount' = $vm.StorageProfile.DataDisks.Count
                'Status' = $null
                'ProvisioningState' = $vm.ProvisioningState
                'Publisher' = $vm.StorageProfile.ImageReference.Publisher
                'Offer' = $vm.StorageProfile.ImageReference.Offer
                'SKU' = $vm.StorageProfile.ImageReference.Sku
                'Version' = $vm.StorageProfile.ImageReference.Version
                'LegalSubEntity' = $vm.tags.LegalSubEntity
                'SubDivision' = $vm.tags.SubDivision
                'Department' = $vm.tags.Department
                'CostCenter' = $vm.tags.CostCenter
                'SenType' = $vm.tags.SenType
                'DeployDate' = $vm.tags.DeployDate
                'DeptName' = $vm.tags.DeptName
                'LOB' = $vm.tags.LOB
                'EnvType' = $vm.tags.EnvType
                'Deployer' = $vm.tags.Deployer
                'Sensitivity' = $vm.tags.Sensitivity
                'AvailabilitySet' = $vm.AvailabilitySetReference.Id }
            
            # if they chose to skip getting the status just put NA (runs much quicker without getting status)
            If ($SkipStatus -eq "Y")
            {
                $vmInfo.Status = "NA"
            }
            else 
            {
                $vmStatus = $vm | Get-AzVM -ResourceGroupName $vm.ResourceGroupName -Name $vm.Name -Status
                $vmInfo.Status = $vmStatus.Statuses[1].DisplayStatus 
            }


            $vmobjs += $vmInfo

        }  
    }
    catch
    {
        Write-Host $error[0]
    }
}

#   send the object out to a csv file and finish output
$vmobjs | Export-Csv -NoTypeInformation -Path $file
Write-Host "VM list written to $file"