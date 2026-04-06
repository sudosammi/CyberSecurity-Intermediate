rule Catch_Hacker_String {
    meta:
        author = "sudosammi"
        description = "Detects my specific hacker string"
    strings:
        $malicious_string = "hack_the_planet"
    condition:
        $malicious_string
}
